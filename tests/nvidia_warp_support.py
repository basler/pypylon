"""Shared helpers to detect NVIDIA GPU and Warp availability for tests."""

from __future__ import annotations

import shutil
import subprocess

_NVIDIA_GPU_AVAILABLE: bool | None = None
_NVIDIA_GPU_SKIP_REASON: str | None = None

_WARP_CPU_AVAILABLE: bool | None = None
_WARP_CPU_SKIP_REASON: str | None = None

_CUPY_AVAILABLE: bool | None = None
_CUPY_SKIP_REASON: str | None = None


def nvidia_gpu_available() -> bool:
    """Return True when an NVIDIA GPU with a working CUDA runtime is present."""
    global _NVIDIA_GPU_AVAILABLE, _NVIDIA_GPU_SKIP_REASON
    if _NVIDIA_GPU_AVAILABLE is not None:
        return _NVIDIA_GPU_AVAILABLE

    reason = "NVIDIA GPU not available"

    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(
                ["nvidia-smi", "-L"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                _NVIDIA_GPU_AVAILABLE = True
                _NVIDIA_GPU_SKIP_REASON = ""
                return True
            reason = "nvidia-smi reported no GPUs"
        except Exception as exc:
            reason = "nvidia-smi failed: %s" % exc
    else:
        reason = "nvidia-smi not found"

    try:
        import warp as wp

        wp.init()
        device = "cuda:0"
        probe = wp.empty((1,), dtype=wp.uint8, device=device)
        if hasattr(wp, "synchronize_device"):
            wp.synchronize_device(device)
        elif hasattr(wp, "synchronize"):
            wp.synchronize()
        del probe
        _NVIDIA_GPU_AVAILABLE = True
        _NVIDIA_GPU_SKIP_REASON = ""
        return True
    except ImportError:
        pass
    except Exception as exc:
        reason = "Warp CUDA probe failed: %s" % exc

    try:
        import cupy

        if cupy.cuda.runtime.getDeviceCount() > 0:
            cupy.empty((1,), dtype=cupy.uint8)
            _NVIDIA_GPU_AVAILABLE = True
            _NVIDIA_GPU_SKIP_REASON = ""
            return True
        reason = "CuPy found no CUDA devices"
    except ImportError:
        pass
    except Exception as exc:
        reason = "CuPy CUDA probe failed: %s" % exc

    _NVIDIA_GPU_AVAILABLE = False
    _NVIDIA_GPU_SKIP_REASON = reason
    return False


def nvidia_gpu_skip_reason() -> str:
    if not nvidia_gpu_available():
        return _NVIDIA_GPU_SKIP_REASON or "NVIDIA GPU not available"
    return ""


def warp_cpu_available() -> bool:
    """Return True when NVIDIA Warp is installed and the CPU backend works."""
    global _WARP_CPU_AVAILABLE, _WARP_CPU_SKIP_REASON
    if _WARP_CPU_AVAILABLE is not None:
        return _WARP_CPU_AVAILABLE

    try:
        import warp as wp

        wp.init()
        probe = wp.empty((1,), dtype=wp.uint8, device="cpu")
        del probe
        _WARP_CPU_AVAILABLE = True
        _WARP_CPU_SKIP_REASON = ""
        return True
    except ImportError:
        reason = "NVIDIA Warp is not installed"
    except Exception as exc:
        reason = "NVIDIA Warp CPU runtime is unavailable: %s" % exc

    _WARP_CPU_AVAILABLE = False
    _WARP_CPU_SKIP_REASON = reason
    return False


def warp_cpu_skip_reason() -> str:
    if not warp_cpu_available():
        return _WARP_CPU_SKIP_REASON or "NVIDIA Warp is not available"
    return ""


def require_nvidia_gpu():
    import pytest

    if not nvidia_gpu_available():
        pytest.skip(nvidia_gpu_skip_reason())


def require_warp_cpu():
    import pytest

    if not warp_cpu_available():
        pytest.skip(warp_cpu_skip_reason())
    import warp as wp

    wp.init()
    return wp


def require_warp_cuda(device: str = "cuda:0"):
    """Skip unless Warp is installed and the requested CUDA device works."""
    import pytest

    require_nvidia_gpu()
    wp = pytest.importorskip("warp", reason="NVIDIA Warp is not installed")
    try:
        wp.init()
        probe = wp.empty((1,), dtype=wp.uint8, device=device)
        if hasattr(wp, "synchronize_device"):
            wp.synchronize_device(device)
        elif hasattr(wp, "synchronize"):
            wp.synchronize()
        del probe
    except Exception as exc:
        pytest.skip("NVIDIA Warp CUDA device %r is unavailable: %s" % (device, exc))
    return wp, device


def cupy_available() -> bool:
    """Return True when CuPy is installed with a working CUDA runtime."""
    global _CUPY_AVAILABLE, _CUPY_SKIP_REASON
    if _CUPY_AVAILABLE is not None:
        return _CUPY_AVAILABLE

    if not nvidia_gpu_available():
        _CUPY_AVAILABLE = False
        _CUPY_SKIP_REASON = nvidia_gpu_skip_reason() or "NVIDIA GPU not available"
        return False

    try:
        import cupy

        if cupy.cuda.runtime.getDeviceCount() <= 0:
            raise RuntimeError("CuPy found no CUDA devices")
        cupy.empty((1,), dtype=cupy.uint8)
        _CUPY_AVAILABLE = True
        _CUPY_SKIP_REASON = ""
        return True
    except ImportError:
        reason = "CuPy is not installed"
    except Exception as exc:
        reason = "CuPy CUDA runtime is unavailable: %s" % exc

    _CUPY_AVAILABLE = False
    _CUPY_SKIP_REASON = reason
    return False


def cupy_skip_reason() -> str:
    if not cupy_available():
        return _CUPY_SKIP_REASON or "CuPy is not available"
    return ""


def require_cupy():
    """Skip unless CuPy is installed and the CUDA runtime works."""
    import pytest

    if not cupy_available():
        pytest.skip(cupy_skip_reason())
    import cupy

    return cupy
