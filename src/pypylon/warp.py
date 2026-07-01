"""NVIDIA Warp helpers for pylon grab buffers."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class _PackedFormat:
    bits_per_pixel: int
    packing: str


_PFNC_PACKED_10 = (
    "Mono10p",
    "BayerBG10p",
    "BayerGB10p",
    "BayerRG10p",
    "BayerGR10p",
)
_PFNC_PACKED_12 = (
    "Mono12p",
    "BayerBG12p",
    "BayerGB12p",
    "BayerRG12p",
    "BayerGR12p",
)
_LEGACY_PACKED_10 = ("Mono10packed", "Mono10Packed")
_LEGACY_PACKED_12 = (
    "Mono12packed",
    "Mono12Packed",
    "BayerBG12Packed",
    "BayerGB12Packed",
    "BayerRG12Packed",
    "BayerGR12Packed",
)

_FORMATS_BY_NAME = {
    **{name.lower(): _PackedFormat(10, "pfnc") for name in _PFNC_PACKED_10},
    **{name.lower(): _PackedFormat(12, "pfnc") for name in _PFNC_PACKED_12},
    **{name.lower(): _PackedFormat(10, "legacy") for name in _LEGACY_PACKED_10},
    **{name.lower(): _PackedFormat(12, "legacy") for name in _LEGACY_PACKED_12},
}
_PYLON_ATTR_FORMATS = {
    **{f"PixelType_{name}": _PackedFormat(10, "pfnc") for name in _PFNC_PACKED_10},
    **{f"PixelType_{name}": _PackedFormat(12, "pfnc") for name in _PFNC_PACKED_12},
    "PixelType_Mono10packed": _PackedFormat(10, "legacy"),
    "PixelType_Mono12packed": _PackedFormat(12, "legacy"),
    **{
        f"PixelType_{name}": _PackedFormat(12, "legacy")
        for name in _LEGACY_PACKED_12
        if name.startswith("Bayer")
    },
}
_FORMATS_BY_PYLON_VALUE: dict[int, _PackedFormat] | None = None
_KERNELS: tuple[Any, Any] | None = None


def supported_packed_pixel_formats() -> tuple[str, ...]:
    """Return the pylon pixel-format names supported by the Warp unpack helper."""
    return tuple(
        dict.fromkeys(
            _PFNC_PACKED_10
            + _PFNC_PACKED_12
            + _LEGACY_PACKED_10
            + _LEGACY_PACKED_12
        )
    )


def unpack_to_uint16(
    src,
    pixel_format,
    width: int,
    height: int,
    *,
    src_stride_bytes: int | None = None,
    output=None,
    device=None,
    synchronize: bool = False,
):
    """Unpack pylon Mono/Bayer 10-bit or 12-bit packed raw bytes to uint16.

    ``src`` must contain the raw bytes for a packed pylon Mono/Bayer image. It
    can be a Warp uint8 array or an object accepted by ``warp.array``. The return
    value is a shaped ``warp.array`` with shape ``(height, width)`` and
    ``dtype=warp.uint16``.

    PFNC ``...p`` formats use a continuous little-endian packed bit stream.
    Legacy pylon ``...packed``/``...Packed`` formats use the older two-pixels
    per three-byte group layout.
    """
    fmt = _resolve_format(pixel_format)
    wp = _require_warp()
    width = int(width)
    height = int(height)
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    src_stride_bytes = (
        _default_src_stride_bytes(width, fmt)
        if src_stride_bytes is None
        else int(src_stride_bytes)
    )
    min_stride = _default_src_stride_bytes(width, fmt)
    if src_stride_bytes < min_stride:
        raise ValueError(
            "src_stride_bytes is too small for width and pixel format: "
            f"{src_stride_bytes} < {min_stride}"
        )

    src = _as_warp_uint8_array(wp, src, device)
    if device is None:
        device = getattr(src, "device", None)

    if output is None:
        output = wp.empty((height, width), dtype=wp.uint16, device=device)
    elif tuple(output.shape) != (height, width):
        raise ValueError(
            f"output shape must be {(height, width)}, got {tuple(output.shape)}"
        )
    elif output.dtype != wp.uint16:
        raise TypeError("output dtype must be warp.uint16")

    pfnc_kernel, legacy_kernel = _get_kernels(wp)
    kernel = pfnc_kernel if fmt.packing == "pfnc" else legacy_kernel
    wp.launch(
        kernel,
        dim=width * height,
        inputs=[src, output, width, height, fmt.bits_per_pixel, src_stride_bytes],
        device=device,
    )
    if synchronize:
        _synchronize(wp, device)
    return output


def _require_warp():
    return import_module("warp")


def _as_warp_uint8_array(wp, src, device):
    if getattr(src, "dtype", None) == wp.uint8:
        array = src
    else:
        array = wp.array(data=src, dtype=wp.uint8, device=device)
    if len(tuple(array.shape)) != 1:
        array = array.reshape((int(array.size),))
    return array


def _resolve_format(pixel_format) -> _PackedFormat:
    if isinstance(pixel_format, str):
        name = pixel_format
        if name.startswith("PixelType_"):
            name = name[len("PixelType_") :]
        try:
            return _FORMATS_BY_NAME[name.lower()]
        except KeyError as exc:
            raise ValueError(f"unsupported packed pixel format: {pixel_format!r}") from exc

    formats_by_value = _formats_by_pylon_value()
    try:
        return formats_by_value[int(pixel_format)]
    except KeyError as exc:
        raise ValueError(f"unsupported packed pixel format: {pixel_format!r}") from exc


def _formats_by_pylon_value() -> dict[int, _PackedFormat]:
    global _FORMATS_BY_PYLON_VALUE
    if _FORMATS_BY_PYLON_VALUE is not None:
        return _FORMATS_BY_PYLON_VALUE

    try:
        pylon = import_module("pypylon.pylon")
    except ImportError:
        _FORMATS_BY_PYLON_VALUE = {}
        return _FORMATS_BY_PYLON_VALUE

    formats_by_value = {}
    for attr, fmt in _PYLON_ATTR_FORMATS.items():
        if hasattr(pylon, attr):
            formats_by_value[int(getattr(pylon, attr))] = fmt
    _FORMATS_BY_PYLON_VALUE = formats_by_value
    return formats_by_value


def _default_src_stride_bytes(width: int, fmt: _PackedFormat) -> int:
    if fmt.packing == "pfnc":
        return (width * fmt.bits_per_pixel + 7) // 8
    return ((width + 1) // 2) * 3


def _get_kernels(wp):
    global _KERNELS
    if _KERNELS is not None:
        return _KERNELS

    @wp.kernel
    def _unpack_pfnc_lsb_kernel(
        src: wp.array(dtype=wp.uint8),
        dst: wp.array2d(dtype=wp.uint16),
        width: int,
        height: int,
        bits_per_pixel: int,
        src_stride_bytes: int,
    ):
        index = wp.tid()
        row = index // width
        col = index - row * width
        if row >= height:
            return

        bit_offset = col * bits_per_pixel
        byte_offset = row * src_stride_bytes + bit_offset // 8
        shift = bit_offset - (bit_offset // 8) * 8
        mask = (wp.uint32(1) << wp.uint32(bits_per_pixel)) - wp.uint32(1)
        word = (
            wp.uint32(src[byte_offset])
            | (wp.uint32(src[byte_offset + 1]) << wp.uint32(8))
        )
        dst[row, col] = wp.uint16((word >> wp.uint32(shift)) & mask)

    @wp.kernel
    def _unpack_legacy_grouped_kernel(
        src: wp.array(dtype=wp.uint8),
        dst: wp.array2d(dtype=wp.uint16),
        width: int,
        height: int,
        bits_per_pixel: int,
        src_stride_bytes: int,
    ):
        index = wp.tid()
        row = index // width
        col = index - row * width
        if row >= height:
            return

        group_offset = row * src_stride_bytes + (col // 2) * 3
        b0 = wp.uint32(src[group_offset])
        b1 = wp.uint32(src[group_offset + 1])
        b2 = wp.uint32(src[group_offset + 2])
        if bits_per_pixel == 12:
            if (col & 1) == 0:
                dst[row, col] = wp.uint16(
                    (b0 << wp.uint32(4)) | (b1 & wp.uint32(15))
                )
            else:
                dst[row, col] = wp.uint16(
                    (b2 << wp.uint32(4)) | (b1 >> wp.uint32(4))
                )
        else:
            if (col & 1) == 0:
                dst[row, col] = wp.uint16(
                    (b0 << wp.uint32(2)) | (b1 & wp.uint32(3))
                )
            else:
                dst[row, col] = wp.uint16(
                    (b2 << wp.uint32(2))
                    | ((b1 >> wp.uint32(4)) & wp.uint32(3))
                )

    _KERNELS = (_unpack_pfnc_lsb_kernel, _unpack_legacy_grouped_kernel)
    return _KERNELS


def _synchronize(wp, device) -> None:
    if hasattr(wp, "synchronize_device"):
        wp.synchronize_device(device)
    elif hasattr(wp, "synchronize"):
        wp.synchronize()


__all__ = ["supported_packed_pixel_formats", "unpack_to_uint16"]
