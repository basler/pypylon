![pypylon](https://raw.githubusercontent.com/basler/pypylon/9303da0cadc10e56d6f6de01b422976c9638c7c5/docs/images/Pypylon_grey_RZ_400px.png "pypylon")

The official python wrapper for the Basler pylon Camera Software Suite.

Background information about usage of pypylon, programming samples and jupyter notebooks can also be found at [pypylon-samples](https://github.com/basler/pypylon-samples).

**Please Note:**
This project is offered with limited technical support by Basler AG.
You are welcome to post any questions or issues on [GitHub](https://github.com/basler/pypylon).
For additional technical assistance, please reach out to our official [Support](https://www.baslerweb.com/en/support/contact) team.

[![Build Status](https://github.com/basler/pypylon/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/basler/pypylon/actions/workflows/main.yml)

# Getting Started

 * Install [pylon](https://www.baslerweb.com/pylon)
   This is strongly recommended but not mandatory. See [known issues](#known-issues) for further details.
 * Install pypylon: ```pip3 install pypylon```
   For more installation options and the supported systems please read the [Installation](#Installation) paragraph.
 * Look at [samples/grab.py](https://github.com/basler/pypylon/blob/master/samples/grab.py) or use the following snippet:

```python
from pypylon import pylon

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# demonstrate some feature access
new_width = camera.Width.Value - camera.Width.Inc
if new_width >= camera.Width.Min:
    camera.Width.Value = new_width

numberOfImagesToGrab = 100
camera.StartGrabbingMax(numberOfImagesToGrab)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        print("SizeX: ", grabResult.Width)
        print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        print("Gray value of first pixel: ", img[0, 0])

    grabResult.Release()
camera.Close()
```

## Getting Started with pylon Data Processing

 * pypylon additionally supports the pylon Data Processing API extension.
 * The [pylon Workbench](https://docs.baslerweb.com/overview-of-the-workbench) allows you to create image processing designs using a graphical editor.
 * Hint: The [pylondataprocessing_tests](https://github.com/basler/pypylon/blob/master/tests/pylondataprocessing_tests) can optionally be used as a source of information about the syntax of the API.
 * Look at [samples/dataprocessing_barcode.py](https://github.com/basler/pypylon/blob/master/samples/dataprocessing_barcode.py) or use the following snippet:

```python
from pypylon import pylondataprocessing
import os

resultCollector = pylondataprocessing.GenericOutputObserver()
recipe = pylondataprocessing.Recipe()
recipe.Load('dataprocessing_barcode.precipe')
recipe.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append);
recipe.Start()

for i in range(0, 100):
    if resultCollector.GetWaitObject().Wait(5000):
        result = resultCollector.RetrieveResult()
        # Print the barcodes
        variant = result["Barcodes"]
        if not variant.HasError():
            # Print result data
            for barcodeIndex in range(0, variant.NumArrayValues):
                print(variant.GetArrayValue(barcodeIndex).ToString())
        else:
            print("Error: " + variant.GetErrorDescription())
    else:
        print("Result timeout")
        break

recipe.Unload()
```

# Update your code to pypylon >= 3.0.0

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

# Installation
## Prerequisites
 * Installed [pylon](https://www.baslerweb.com/pylon)
   For the binary installation this is not mandatory but strongly recommended. See [known issues](#known-issues) for further details.
 * Installed [python](https://www.python.org/) with [pip](https://pip.pypa.io/en/stable/)
 * Installed [CodeMeter Runtime](https://www.wibu.com/support/user/user-software.html) when you want to use pylon vTools and the pylon Data Processing API extension on your platform.

## pylon OS Versions and Features
Please note that the pylon Camera Software Suite may support different operating system versions and features than pypylon.
For latest information on pylon refer to: https://www.baslerweb.com/en/software/pylon/
In addition, check the release notes of your pylon installation. 
For instance: 
* pylon Camera Software Suite 8.1.0 supports Windows 10/11 64 bit, Linux x86_64 and Linux aarch64 with glibc version >= 2.31 or newer,
  macOS Sonoma or newer.
* pylon vTools are supported on pylon 7.0.0 and newer.
* pylon vTools are supported on pypylon 3.0 and newer only on Windows 10/11 64 bit, Linux x86_64 and Linux aarch64. 
* For pylon vTools that require a license refer to: https://www.baslerweb.com/en/software/pylon-vtools/
* CXP-12: To use CXP with pypylon >= 4.0.0 you need to install the CXP GenTL producer and drivers using the pylon Camera Software Suite setup.
* For accessing Basler 3D cameras, e.g. Basler blaze, installation of pylon Camera Software Suite 8.1.0 
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

## Starting Development
```console
python setup.py develop
```
This will "link" the local pypylon source directory into your python installation. It will not package the pylon libraries and always use the installed pylon.
After changing pypylon, execute `python setup.py build` and test...

## Running Unit Tests
> NOTE: The unit tests try to import `pypylon....`, so they run against the *installed* version of pypylon.
```console
pytest tests/....
```

# Known Issues
 * For USB 3.0 cameras to work on Linux, you need to install appropriate udev rules.
   The easiest way to get them is to install the official [pylon](http://www.baslerweb.com/pylon) package.
