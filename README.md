<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/pylon_basler_banner_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/images/pylon_basler_banner.svg">
  <img alt="Basler pypylon banner" src="https://raw.githubusercontent.com/basler/pypylon/master/docs/images/pylon_basler_banner.svg">
</picture>

<br>
pypylon is the official Python language binding for the Basler pylon C++ APIs. It enables Python applications to control and acquire images from Basler machine vision products, e.g. cameras. Furthermore, the pylon Data Processing API allows you to perform image processing tasks.

> **Note:** This README was updated for pypylon 26.6.
> pypylon 26.6 introduces breaking changes. While most existing code is expected to remain functional, check the [changelog](https://github.com/basler/pypylon/blob/master/changelog.txt) for a full list of affected areas.

Background information about usage of pypylon, programming samples and jupyter notebooks can also be found at [pypylon-samples](https://github.com/basler/pypylon-samples) *(may not always reflect the latest pypylon API/style)*.

[![Build Status](https://github.com/basler/pypylon/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/basler/pypylon/actions/workflows/main.yml)

# Getting Started
> **Coming soon:** A detailed pypylon Programmer's Guide will be available [here](https://github.com/basler/pypylon/blob/master/docs/programmers_guide).

 * Install [pylon](https://www.baslerweb.com/pylon)
   This is strongly recommended but not mandatory. See [known issues](#known-issues) for further details.
 * Install pypylon: ```pip3 install pypylon```
   For more installation options and the supported systems please read the [Installation](#Installation) paragraph.
 * Look at [samples/pylon/grab/grab.py](https://github.com/basler/pypylon/blob/master/samples/pylon/grab/grab.py) or use the following snippet:

```python
from pypylon import pylon

# Create an InstantCamera object with the camera device found first.
# The with statement creates, opens the camera and destroys it automatically.
with pylon.InstantCamera(pylon.FirstFound) as camera:
    print("Using device:", camera.DeviceInfo.ModelName)

    # Demonstrate some feature access using the pylon parameter API.
    camera.Width.TrySetToMaximum()

    # Start the grabbing of 100 images.
    camera.StartGrabbingMax(100)

    while camera.IsGrabbing():
        # The grab result is released automatically at the end of the with block.
        with camera.RetrieveResult(
            5000, pylon.TimeoutHandling_ThrowException
        ) as grab_result:
            if grab_result.GrabSucceeded():
                # Some camera models use a GenICam Generic Data Container (GenDC) format.
                # For single grabbed images, a data component is emulated automatically.
                with grab_result.GetFirstImageDataComponent() as image_data_component:
                        # Access the image data.
                        img = image_data_component.Array
                        print(f"SizeX: {image_data_component.Width};"
                              f"SizeY: {image_data_component.Height}; "
                              f"Gray value of first pixel: {img[0, 0]}")
```

## Getting Started with pylon Data Processing

 * pypylon additionally supports the pylon Data Processing API extension.
 * The [pylon Workbench](https://docs.baslerweb.com/overview-of-the-workbench) allows you to create image processing designs using a graphical editor.
 * Hint: The [pylondataprocessing tests](https://github.com/basler/pypylon/blob/master/tests/pylondataprocessing) can optionally be used as a source of information about the syntax of the API.
 * Look at [samples/pylondataprocessing/barcode/barcode.py](https://github.com/basler/pypylon/blob/master/samples/pylondataprocessing/barcode/barcode.py) or use the following snippet:

```python
from pypylon import pylon
from pypylon import pylondataprocessing

# This object collects the output data. Create it before the recipe so it outlives it.
result_collector = pylondataprocessing.GenericOutputObserver()

# Create a recipe object representing a recipe file created with the pylon Viewer Workbench.
with pylondataprocessing.Recipe() as recipe:
    recipe.Load("barcode.precipe")
    recipe.RegisterAllOutputsObserver(result_collector, pylon.RegistrationMode_Append)
    recipe.Start()

    for i in range(100):
        if result_collector.WaitObject.Wait(5000):
            result = result_collector.RetrieveResult()
            # Print the barcodes.
            barcodes = result["Barcodes"]
            if not barcodes.HasError():
                for index in range(barcodes.NumArrayValues):
                    print(barcodes[index].ToString())
            else:
                print("Error:", barcodes.ErrorDescription)
        else:
            print("Result timeout")
            break
```

# Update your code to pypylon >= 26.06

The current pypylon implementation allows direct feature assignment:

```python
cam.Gain = 42
```

This assignment style is deprecated with pypylon 3.0.0, as it prevents full typing support for pypylon.

The recommended assignment style is now:

```python
cam.Gain.Value = 42
```

To identify the locations in your code that have to be updated, run with enabled warnings:

`PYTHONWARNINGS=default python script.py`

pypylon now also ships the full pylon parameter API (classes derived from
`Pylon::CParameter`). It adds many convenience methods on parameters, such as
`camera.ExposureTime.SetToMaximum()`, `camera.PixelFormat.TrySetValue("Mono8")`
and `camera.ExposureTime.GetValueOrDefault(default_value)`. In addition,
`pylon.InstantCamera` supports the context manager protocol, so it can be used
in a `with` statement to be opened and closed automatically. See the
[samples](https://github.com/basler/pypylon/tree/master/samples) and the style
guidelines in the [context](https://github.com/basler/pypylon/tree/master/context)
folder for the recommended coding style.

# Installation
## Prerequisites
 * Installed [pylon](https://www.baslerweb.com/pylon)
   For the binary installation this is not mandatory but strongly recommended. See [known issues](#known-issues) for further details.
 * Installed [python](https://www.python.org/) 3.9 or newer with [pip](https://pip.pypa.io/en/stable/)
 * Installed [CodeMeter Runtime](https://www.wibu.com/support/user/user-software.html) when you want to use pylon vTools and the pylon Data Processing API extension on your platform.

## pylon OS Versions and Features
Please note that the pylon Software Suite may support different operating system versions and features than pypylon.
For latest information on pylon refer to: https://www.baslerweb.com/en/software/pylon/
In addition, check the release notes of your pylon installation. 
For instance: 
* pylon Software Suite 26.06 supports Windows 10/11 64 bit, Linux x86_64 and Linux aarch64 with glibc version >= 2.31 or newer,
  macOS Sonoma or newer.
* pylon vTools are supported on pylon 7.0.0 and newer.
* pylon vTools are supported on pypylon 3.0 and newer only on Windows 10/11 64 bit, Linux x86_64 and Linux aarch64. 
* For pylon vTools that require a license refer to: https://www.baslerweb.com/en/software/pylon-vtools/
* CXP-12: To use CXP with pypylon >= 4.0.0 you need to install the CXP GenTL producer and drivers using the pylon Software Suite setup.
* For accessing Basler 3D cameras, e.g. Basler blaze, installation of pylon Software Suite 8.1.0 or newer
  and the latest pylon Supplementary Package for blaze is required.

## Binary Installation
The easiest way to get pypylon is to install a prebuild wheel.
Binary releases for most architectures are available on [pypi](https://pypi.org)**.
To install pypylon open your favourite terminal and run:

```pip3 install pypylon```

The following versions are available on pypi:

 |                | 3.9 | 3.10 | 3.11 | 3.12 | 3.13 |
 |----------------|-----|------|------|------|------|
 | Windows 64bit  | x   | x    |  x   |  x   |  x   |
 | Linux x86_64*  | x   | x    |  x   |  x   |  x   |
 | Linux aarch64* | x   | x    |  x   |  x   |  x   |
 | macOS x86_64** | x   | x    |  x   |  x   |  x   |
 | macOS arm64**  | x   | x    |  x   |  x   |  x   |


> Additional Notes on binary packages:
> * (*) The linux 64bit binaries are manylinux_2_31 conformant.
    This is roughly equivalent to a minimum glibc version >= 2.31. 
    :warning: You need at least pip 20.3 to install them.
> * (**) macOS binaries are built for macOS >= 14.0 (Sonoma)

## Installation from Source
Building the pypylon bindings is supported and tested on Windows, Linux and macOS

You need a few more things to compile pypylon:
 * An installation of pylon SDK for your platform
 * A compiler for your system (Visual Studio on Windows, gcc on linux, xCode commandline tools on macOS)
 * Python 3.9+ development files (e.g. `sudo apt install python3-dev` on linux)
 * [swig](http://www.swig.org) 4.4
   * For all 64bit platforms you can install the tool via `pip install "swig==4.4.1"`

To build pypylon from source:
```console
git clone https://github.com/basler/pypylon.git
cd pypylon
pip install .
```

If pylon SDK is not installed in a default location you have to specify the location from the environment
 * on Linux: `export PYLON_ROOT=<installation directory of pylon SDK>`
 * on macOS: `export PYLON_FRAMEWORK_LOCATION=<framework base folder that contains pylon.framework>`


# Development

Pull requests to pypylon are very welcome. To help you getting started with pypylon improvements, here are some hints:

If you use an AI coding assistant, see [AGENTS.md](AGENTS.md) for the repository map, build/test commands, and coding-style references.

## Starting Development

Use a virtual environment to avoid conflicts with system-managed Python (see [PEP 668](https://peps.python.org/pep-0668/) on many Linux distributions):

```console
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -e .
```

For development including test dependencies:

```console
pip install -e ".[dev]"
```

This gives you an editable install: changes to SWIG (`.i`) files or Python code require a rebuild (`pip install -e .`) before running tests; the installed pylon SDK is used as-is.

## Running Unit Tests
> NOTE: The unit tests import `pypylon`, so they run against the *installed* version in your environment.

Use `python -m pytest` to ensure the correct Python (and thus the correct pypylon) is used. Plain `pytest` may resolve to a different installation (e.g. `~/.local/bin/pytest`) that does not see your virtual environment's packages.

Run the hardware-free (Camera Emulation) suites the same way CI does:
```console
pip install pytest numpy
python -m pytest tests/genicam tests/pylon/emulated tests/pylondataprocessing
```
The `tests/pylon/usb` and `tests/pylon/gigE` suites require real cameras.

Or run all configured tests (see `pyproject.toml`):

```console
python -m pytest
```

Test dependencies (pytest, numpy) are installed with `pip install -e ".[dev]"` or manually: `pip install pytest numpy`.

## Debugging While Developing

### Edit-Rebuild-Test Loop

1. Edit SWIG (`.i`), CMake, or Python sources.
2. Rebuild: `pip install -e .`
3. Run tests: `python -m pytest tests/` or a subset, e.g. `tests/pylon/emulated/`
4. Or run a sample: `python samples/grab.py`, `python samples/helloworld.py`, etc.

### Python-Side Debugging

- **pdb**: Run a script under the debugger:
  ```console
  python -m pdb -m pytest tests/pylon/emulated/version_test.py -v
  ```
- **IDE**: Configure VS Code or PyCharm to use `.venv/bin/python` and set breakpoints in your Python code or in tests.
- **Print debugging**: Add `print()` or `logging` in Python files under `src/pypylon/`; rebuild and re-run.

### Native/C++ Extension Debugging

The extension is a SWIG-generated C++ module. To debug into native code:

1. Build with debug symbols:
   ```console
   pip install -e . --config-settings=cmake.build-type=Debug
   ```
2. Run Python under GDB (Linux) or your platform debugger:
   ```console
   gdb --args python samples/helloworld.py
   ```
   Or attach to a running process: `gdb -p <pid>` then `continue`. In VS Code, use the C/C++ extension and configure it to attach to the Python process.
3. Add logging in the C++ sources or SWIG typemaps; rebuild and run tests or samples.

# Known Issues
 * For USB 3.0 cameras to work on Linux, you need to install appropriate udev rules.
   The easiest way to get them is to install the official [pylon](http://www.baslerweb.com/pylon) package.

# Support
You are welcome to post any questions or issues on [GitHub](https://github.com/basler/pypylon).
For additional technical support for business customers, please reach out to our official [Support](https://www.baslerweb.com/en/support/contact) team.