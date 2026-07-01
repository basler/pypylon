"""Pytest configuration and shared skip rules for optional NVIDIA/Warp/CuPy tests."""

import pytest

from nvidia_warp_support import (
    cupy_available,
    cupy_skip_reason,
    nvidia_gpu_available,
    nvidia_gpu_skip_reason,
    warp_cpu_available,
    warp_cpu_skip_reason,
)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "nvidia: requires an NVIDIA GPU with a working CUDA runtime",
    )
    config.addinivalue_line(
        "markers",
        "warp: requires NVIDIA Warp with a working CPU backend",
    )
    config.addinivalue_line(
        "markers",
        "cupy: requires CuPy with a working CUDA runtime",
    )


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "nvidia" in item.keywords and not nvidia_gpu_available():
            item.add_marker(
                pytest.mark.skip(reason=nvidia_gpu_skip_reason())
            )
        if "warp" in item.keywords and not warp_cpu_available():
            item.add_marker(
                pytest.mark.skip(reason=warp_cpu_skip_reason())
            )
        if "cupy" in item.keywords and not cupy_available():
            item.add_marker(
                pytest.mark.skip(reason=cupy_skip_reason())
            )
