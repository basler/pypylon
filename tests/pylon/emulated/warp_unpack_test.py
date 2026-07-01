"""\
Unit tests for pypylon.warp packed-format unpacking helpers.

These tests require NVIDIA Warp. GPU-backed buffer-factory benchmarks live under
tests/performance/ and are marked nvidia.
"""
import os

import numpy as np
import pytest

from nvidia_warp_support import require_warp_cpu

os.environ.setdefault("WARP_CACHE_PATH", "/tmp/pypylon-warp-cache")

pytestmark = pytest.mark.warp


def _pack_pfnc_lsb(
    values: np.ndarray,
    bits_per_pixel: int,
    row_padding: int = 0,
) -> np.ndarray:
    height, width = values.shape
    stride = (width * bits_per_pixel + 7) // 8 + row_padding
    packed = np.zeros((height, stride), dtype=np.uint8)
    mask = (1 << bits_per_pixel) - 1

    for row in range(height):
        for col in range(width):
            value = int(values[row, col]) & mask
            bit_offset = col * bits_per_pixel
            byte_offset = bit_offset // 8
            shift = bit_offset % 8
            word = value << shift
            packed[row, byte_offset] |= word & 0xFF
            packed[row, byte_offset + 1] |= (word >> 8) & 0xFF

    return packed


def _pack_legacy_grouped(
    values: np.ndarray,
    bits_per_pixel: int,
    row_padding: int = 0,
) -> np.ndarray:
    height, width = values.shape
    stride = ((width + 1) // 2) * 3 + row_padding
    packed = np.zeros((height, stride), dtype=np.uint8)
    mask = (1 << bits_per_pixel) - 1

    for row in range(height):
        for col in range(0, width, 2):
            p0 = int(values[row, col]) & mask
            p1 = int(values[row, col + 1]) & mask if col + 1 < width else 0
            base = (col // 2) * 3
            if bits_per_pixel == 12:
                packed[row, base] = p0 >> 4
                packed[row, base + 1] = (p0 & 0x0F) | ((p1 & 0x0F) << 4)
                packed[row, base + 2] = p1 >> 4
            else:
                packed[row, base] = p0 >> 2
                packed[row, base + 1] = (p0 & 0x03) | ((p1 & 0x03) << 4)
                packed[row, base + 2] = p1 >> 2

    return packed


@pytest.mark.parametrize(
    ("pixel_format", "bits_per_pixel"),
    [
        ("Mono10p", 10),
        ("BayerRG10p", 10),
        ("Mono12p", 12),
        ("BayerGB12p", 12),
    ],
)
def test_warp_unpack_pfnc_packed_to_uint16(pixel_format, bits_per_pixel):
    wp = require_warp_cpu()
    from pypylon import warp as pylon_warp

    values = np.array(
        [
            [0, 1, (1 << bits_per_pixel) - 1, 17, 511],
            [3, 19, 257, 1023, 5],
        ],
        dtype=np.uint16,
    ) & np.uint16((1 << bits_per_pixel) - 1)
    packed = _pack_pfnc_lsb(values, bits_per_pixel)
    src = wp.array(data=packed.reshape(-1), dtype=wp.uint8, device="cpu")

    out = pylon_warp.unpack_to_uint16(
        src,
        pixel_format,
        values.shape[1],
        values.shape[0],
        synchronize=True,
    )

    np.testing.assert_array_equal(out.numpy(), values)


@pytest.mark.parametrize(
    ("pixel_format", "bits_per_pixel"),
    [
        ("Mono10packed", 10),
        ("Mono12packed", 12),
        ("BayerRG12Packed", 12),
    ],
)
def test_warp_unpack_legacy_packed_to_uint16(pixel_format, bits_per_pixel):
    wp = require_warp_cpu()
    from pypylon import warp as pylon_warp

    values = np.array(
        [
            [0, 1, (1 << bits_per_pixel) - 1],
            [7, 33, 129],
            [511, 13, 21],
        ],
        dtype=np.uint16,
    ) & np.uint16((1 << bits_per_pixel) - 1)
    packed = _pack_legacy_grouped(values, bits_per_pixel)
    src = wp.array(data=packed.reshape(-1), dtype=wp.uint8, device="cpu")

    out = pylon_warp.unpack_to_uint16(
        src,
        pixel_format,
        values.shape[1],
        values.shape[0],
        synchronize=True,
    )

    np.testing.assert_array_equal(out.numpy(), values)


def test_warp_unpack_respects_source_stride_padding():
    wp = require_warp_cpu()
    from pypylon import warp as pylon_warp

    values = np.array([[0, 1, 2, 3], [4095, 17, 33, 63]], dtype=np.uint16)
    packed = _pack_pfnc_lsb(values, bits_per_pixel=12, row_padding=5)
    src = wp.array(data=packed.reshape(-1), dtype=wp.uint8, device="cpu")

    out = pylon_warp.unpack_to_uint16(
        src,
        "Mono12p",
        values.shape[1],
        values.shape[0],
        src_stride_bytes=packed.shape[1],
        synchronize=True,
    )

    np.testing.assert_array_equal(out.numpy(), values)


def test_warp_unpack_accepts_pylon_pixel_type_constant():
    wp = require_warp_cpu()
    from pypylon import pylon
    from pypylon import warp as pylon_warp

    values = np.array([[0, 1, 4095, 17]], dtype=np.uint16)
    packed = _pack_pfnc_lsb(values, bits_per_pixel=12)
    src = wp.array(data=packed.reshape(-1), dtype=wp.uint8, device="cpu")

    out = pylon_warp.unpack_to_uint16(
        src,
        pylon.PixelType_Mono12p,
        values.shape[1],
        values.shape[0],
        synchronize=True,
    )

    np.testing.assert_array_equal(out.numpy(), values)


def test_warp_unpack_rejects_unsupported_pixel_format():
    from pypylon import warp as pylon_warp

    with pytest.raises(ValueError, match="unsupported packed pixel format"):
        pylon_warp.unpack_to_uint16(bytearray(4), "Mono8", 2, 2)
