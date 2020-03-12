# pypylon
The official python wrapper for the Basler pylon Camera Software Suite.

**Please Note:**
This project is offered with no technical support by Basler AG.
You are welcome to post any questions or issues on [GitHub](https://github.com/basler/pypylon) or on [ImagingHub](https://www.imaginghub.com).

[![Build Status](https://travis-ci.org/basler/pypylon.svg?branch=master)](https://travis-ci.org/basler/pypylon)
[![Build status](https://ci.appveyor.com/api/projects/status/45j4tydwdr0fv05p/branch/master?svg=true)](https://ci.appveyor.com/project/basler-oss/pypylon/branch/master)

# For the Impatient
 * Install [pylon](https://www.baslerweb.com/pylon).
 * Download a binary wheel from the [releases](https://github.com/Basler/pypylon/releases) page.
 * Install the wheel using ```pip3 install <your downloaded wheel>.whl```
 * Look at samples/grab.py in this repository

# Installation
## Prerequisites
 * Installed [pylon](https://www.baslerweb.com/pylon).
 * Installed [python](https://www.python.org/) (python 3 recommended).
 * Installed [pip](https://pip.pypa.io/en/stable/).

## Binary Installation
The easiest way to get pypylon is to install a prebuild wheel.

Binary releases are available on the [releases](https://github.com/Basler/pypylon/releases) page.

## Installation from Source
Building the pypylon bindings is supported and tested on Windows and Linux.

You need a few more things to compile pypylon:
 * A compiler for your system (Visual Studio on Windows, gcc on linux)
 * [swig](http://www.swig.org) >= 3.0.12

To build pypylon from source:
```
git clone https://github.com/basler/pypylon.git
cd pypylon
pip install .
```

# Getting Started
## Hello World
See the [grab sample](https://github.com/basler/pypylon/blob/master/samples/grab.py) in the samples directory.

Excerpt:

```
from pypylon import pylon

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# demonstrate some feature access
new_width = camera.Width.GetValue() - camera.Width.GetInc()
if new_width >= camera.Width.GetMin():
    camera.Width.SetValue(new_width)

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

# Development

Pull requests to pypylon are very welcome. To help you getting started with pypylon improvements, here are some hints:

## Starting Development
```
python setup.py develop
```
This will "link" the local pypylon source directory into your python installation. It will not package the pylon libraries and always use the installed pylon.
After changing pypylon, execute `python setup.py build` and test...

## Running Unit Tests
> NOTE: The unit tests try to import `pypylon....`, so they run against the *installed* version of pypylon.
```
python -m unittest tests/....
python tests/....
```
# Known Issues
 * For USB 3.0 cameras to work on Linux, you need to install appropriate udev rules.
   The easiest way to get them is to install an official pylon package from http://www.baslerweb.com/pylon.
