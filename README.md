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
> A detailed pypylon Programmer's Guide is available [here](https://github.com/basler/pypylon/blob/master/docs/programmers_guide).

 * Install [pylon](https://www.baslerweb.com/pylon)
   This is strongly recommended but not mandatory. See [known issues](#known-issues) for further details.
 * Install pypylon: ```pip3 install pypylon```
   For more installation options and the supported systems please read the [Installation](#installation) paragraph.
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

## Buffer Factories and Zero-Copy Array Access

Runnable sample:
[samples/pylon/grab_buffer_factory/grab_buffer_factory.py](samples/pylon/grab_buffer_factory/grab_buffer_factory.py)

pypylon 26.6 adds several ways to work with image data. They compose with custom
buffer factories — choose based on lifetime, payload type, and whether you need
the allocator's native Python object.

### Copying access (default, always safe)

| API | Use when |
|-----|----------|
| `component.Array` / `grab_result.Array` | You need data that outlives the grab result |
| `component.GetArray()` / `grab_result.GetArray()` | Same; explicit method form |
| `ImageFormatConverter.Convert(src).Array` | Converted result as a new `PylonImage` copy |

These work with or without a `PythonBufferFactory`.

### Scoped zero-copy (recommended on master)

`GetArrayZeroCopy()` is the standard zero-copy API on `GrabResult`,
`PylonDataComponent`, and `PylonImage`. The view is valid only inside the
`with` block; holding it past that scope raises `RuntimeError`.

```python
with grab_result.GetFirstImageDataComponent() as component:
    with component.GetArrayZeroCopy() as view:
        process(view)
```

Use this path for **both classic image payloads and GenDC** — always reach the
image through `GetFirstImageDataComponent()` (or `DataContainer`) rather than
treating the grab result as a flat image. Works with custom buffer factories
because the grab result keeps the factory-allocated buffer alive.

Related master APIs that produce **independent** output buffers (not views into
the grab buffer):

* `ImageFormatConverter.ConvertToArray(src)` — convert into a pre-allocated NumPy
  array while `src` is still valid. Accepts `GrabResult`, `PylonDataComponent`,
  and `PylonImage`. See
  [samples/pylon/utility_image_format_converter/utility_image_format_converter.py](samples/pylon/utility_image_format_converter/utility_image_format_converter.py).
* `ImagePersistence.SaveArray(...)` — save a NumPy array without creating a
  `PylonImage` first.

### Persistent zero-copy views (buffer-factory extension)

When a view must **outlive the current scope** but stay tied to the grab buffer,
use the buffer-factory view API on `GrabResult`:

```python
view = grab_result.GetArray(copy=False)   # same as GetArrayView()
```

The returned object keeps the `GrabResult` alive until it is released. Prefer
`GetArrayZeroCopy()` when the view stays in one scope; use `copy=False` for
hand-offs to other functions or threads. Holding too many views can stall
acquisition because pylon cannot recycle grab buffers.

`GetArrayZeroCopy()` and `GetArray(copy=False)` both work with a custom factory
that allocates ordinary host memory. They are not interchangeable when the
factory returns a **non-NumPy owner** (pinned Warp memory, CUDA arrays): use
`GetBufferOwnerView()` instead (see GPU samples below).

### Python buffer factories

`InstantCamera.SetBufferFactory()` makes the camera grab into memory your Python
code provides:

```python
factory = pylon.PythonBufferFactory(allocate, free)
camera.SetBufferFactory(factory, pylon.Cleanup_None)
```

The allocation callback returns `(address, keepalive[, context[, capacity]])`.
pylon keeps `keepalive` alive until the buffer is freed.

| API | Role with a buffer factory |
|-----|---------------------------|
| `GetBufferOwner()` | The `keepalive` object for the current grab buffer, resolved from the factory-local owner map |
| `GetBufferOwnerView(raw=False)` | Shape that owner as an image and keep the grab result alive. GenDC returns an image-component view because the owner contains the full container |
| `GetArrayZeroCopy()` | Scoped NumPy view into grab/component memory (any allocator) |
| `GetArray(copy=False)` | Persistent NumPy view; best with host-memory factories |
| `ConvertToArray(component)` | Reads from live grab/component; writes to a new owned array |

For GenDC (`PayloadType_GenDC`) the factory allocates the **full container**.
Access components via `GetFirstImageDataComponent()` or `DataContainer`, as in
[samples/pylon/grab_data_container/grab_data_container.py](samples/pylon/grab_data_container/grab_data_container.py).
Grab-result image APIs resolve the first image component, matching the pylon C++
`IImage` adapter; `GetBufferOwner()` still returns the full-container owner.

The factory retains each Python owner until pylon calls `FreeBuffer`.
`GetBufferOwner()` works for results returned by `RetrieveResult`/`GrabOne` and
inside `OnImageGrabbed`; owner lookup is factory-local and does not add a second,
process-wide owning reference.

With `Cleanup_None`, pypylon keeps replaced factories retired until
`DestroyDevice()` so delayed `FreeBuffer` calls remain valid. Applications
should still stop grabbing and release all grab results and persistent views
before clearing the factory or destroying the device. `Cleanup_Delete` transfers
the C++ factory lifetime to pylon; do not use its SWIG proxy after detaching it.

### Optional: NVIDIA Warp and CUDA

[samples/pylon/grab_warp_pinned/](samples/pylon/grab_warp_pinned/grab_warp_pinned.py)
and [samples/pylon/grab_warp_packed_unpack/](samples/pylon/grab_warp_packed_unpack/grab_warp_packed_unpack.py)
use `GetBufferOwnerView()` because the factory returns Warp pinned arrays with
`__cuda_array_interface__`, not plain NumPy buffers. Install Warp
(`pip install warp-lang`) and run:

```console
python samples/pylon/grab_warp_pinned/grab_warp_pinned.py
python samples/pylon/grab_warp_packed_unpack/grab_warp_packed_unpack.py
```

### Buffer lifetime tests

[tests/pylon/emulated/instantcamera_test.py](tests/pylon/emulated/instantcamera_test.py)
covers factory allocation, `GetArrayZeroCopy()` with custom buffers, and
`GetArray(copy=False)` backpressure across threads. CUDA owner proxies are in
[tests/pylon/emulated/cupy_buffer_factory_test.py](tests/pylon/emulated/cupy_buffer_factory_test.py)
(marked `nvidia` and `cupy`; skipped without GPU/CuPy).

Optional Warp benchmarks: `tests/performance/test_warp_bufferfactory_perf.py`

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
 * Installed [python](https://www.python.org/) with [pip](https://pip.pypa.io/en/stable/)
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

Prebuilt pypylon wheels on PyPI are available for the Python versions and platforms listed below:

 |                | 3.9 | 3.10 | 3.11 | 3.12 | 3.13 | 3.14 |
 |----------------|-----|------|------|------|------|------|
 | Windows 64bit  | x   | x    |  x   |  x   |  x   |  x   |
 | Linux x86_64*  | x   | x    |  x   |  x   |  x   |  x   |
 | Linux aarch64* | x   | x    |  x   |  x   |  x   |  x   |
 | macOS x86_64** | x   | x    |  x   |  x   |  x   |  x   |
 | macOS arm64**  | x   | x    |  x   |  x   |  x   |  x   |


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
 * Python development files (e.g. `sudo apt install python-dev` on linux)
 * [swig](http://www.swig.org) 4.3
   * For all 64bit platforms you can install the tool via `pip install "swig==4.3"`

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

If you use an AI coding assistant, see [AGENTS.md](https://github.com/basler/pypylon/blob/master/AGENTS.md) for the repository map, build/test commands, and coding-style references.

## Starting Development
```console
python setup.py develop
```
This will "link" the local pypylon source directory into your python installation. It will not package the pylon libraries and always use the installed pylon.
After changing pypylon, execute `python setup.py build` and test...

## Running Unit Tests
> NOTE: The unit tests try to import `pypylon....`, so they run against the *installed* version of pypylon.

Run the hardware-free (Camera Emulation) suites the same way CI does:
```console
pip install pytest numpy
pytest tests/genicam tests/pylon/emulated tests/pylondataprocessing
```
The `tests/pylon/usb` and `tests/pylon/gigE` suites require real cameras.

Optional Warp GPU buffer-factory benchmarks require NVIDIA Warp, a CUDA-capable
system, and `pytest-benchmark`:

```console
pip install pytest-benchmark warp-lang
python -m pytest tests/performance/test_warp_bufferfactory_perf.py --benchmark-json warp-bufferfactory.json
```

# Known Issues
 * For USB 3.0 cameras to work on Linux, you need to install appropriate udev rules.
   The easiest way to get them is to install the official [pylon](http://www.baslerweb.com/pylon) package.

# Support
You are welcome to post any questions or issues on [GitHub](https://github.com/basler/pypylon).
For additional technical support for business customers, please reach out to our official [Support](https://www.baslerweb.com/en/support/contact) team.