"""setuptools_scm local version scheme: append +pylonX.Y.Z for non-reference SDK builds."""

from __future__ import annotations

import glob
import os
import platform
import re
import subprocess
import sys
from typing import Optional

REFERENCE_PYLON_VERSION = {
    "Windows": "12.2.0",
    "Linux": "12.2.0",
    "Linux_armv7l": "6.2.0",
    "Darwin": "12.2.0",
}


def _platform_key() -> str:
    system = platform.system()
    if system == "Linux" and platform.machine() == "armv7l":
        return "Linux_armv7l"
    if system in REFERENCE_PYLON_VERSION:
        return system
    return system


def _reference_version() -> str:
    return REFERENCE_PYLON_VERSION.get(_platform_key(), "12.2.0")


def _run_pylon_config(config_path: str) -> Optional[str]:
    if not os.path.isfile(config_path):
        return None
    try:
        version = subprocess.check_output(
            [config_path, "--version"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    if version == "9...":
        return "9.0.3.215"
    return version or None


def _linux_pylon_version() -> Optional[str]:
    root = os.environ.get("PYLON_ROOT", "/opt/pylon")
    return _run_pylon_config(os.path.join(root, "bin", "pylon-config"))


def _macos_pylon_version() -> Optional[str]:
    framework_base = os.environ.get("PYLON_FRAMEWORK_LOCATION", "/Library/Frameworks")
    if not framework_base or framework_base == "undef":
        framework_base = "/Library/Frameworks"
    config = os.path.join(
        framework_base,
        "pylon.framework",
        "Versions",
        "Current",
        "Resources",
        "Tools",
        "pylon-config",
    )
    return _run_pylon_config(config)


def _windows_pylon_version() -> Optional[str]:
    dev_dir = os.environ.get("PYLON_DEV_DIR")
    if not dev_dir and sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Basler\pylon") as key:
                install_folder = winreg.QueryValueEx(key, "InstallationFolder")[0]
            candidate = os.path.join(install_folder, "Development")
            if os.path.isdir(candidate):
                dev_dir = candidate
        except OSError:
            pass
    if not dev_dir:
        return None

    arch = "x64" if platform.machine().endswith("64") else "Win32"
    dll_dir = os.path.realpath(os.path.join(dev_dir, "..", "Runtime", arch))
    matches = glob.glob(os.path.join(dll_dir, "PylonBase_*.dll"))
    if not matches:
        return None

    import ctypes

    dll_path = matches[0]
    prev_path = os.environ.get("PATH", "")
    os.environ["PATH"] = os.pathsep.join((dll_dir, prev_path))
    try:
        pylon_version = [ctypes.c_uint() for _ in range(4)]
        pylon_base = ctypes.CDLL(dll_path)
        pylon_base.GetPylonVersion(*[ctypes.byref(v) for v in pylon_version])
        return ".".join(str(v.value) for v in pylon_version)
    except OSError:
        return None
    finally:
        os.environ["PATH"] = prev_path


def get_pylon_sdk_version() -> Optional[str]:
    system = platform.system()
    if system == "Linux":
        return _linux_pylon_version()
    if system == "Darwin":
        return _macos_pylon_version()
    if system == "Windows":
        return _windows_pylon_version()
    return None


def pylon_sdk_local_suffix() -> str:
    pylon_version = get_pylon_sdk_version()
    if not pylon_version:
        return ""

    match = re.match(r"^(\d+\.\d+\.\d+)\.\d+(.*)", pylon_version)
    if not match:
        return ""

    pylon_version_no_build = match.group(1)
    pylon_version_tag = match.group(2)
    reference_version = _reference_version()

    if pylon_version_no_build == reference_version and pylon_version_tag == "":
        return ""

    tag_cleaned = re.sub(r"[^a-zA-Z0-9.\-_]", "", pylon_version_tag)
    return f"pylon{pylon_version_no_build}{tag_cleaned}"


def pylon_local_version(version) -> str:
    pylon_part = pylon_sdk_local_suffix()
    if pylon_part:
        return pylon_part

    from setuptools_scm.version import get_local_dirty_tag

    dirty = get_local_dirty_tag(version)
    if dirty:
        return dirty.lstrip("+")
    if version.distance and version.node:
        return f"g{version.node}"
    return ""
