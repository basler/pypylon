# Installation and Environment Setup

This topic covers describes the installation of pypylon and how to verify it.

For background information about pypylon, see the [Introduction](pypylon-introduction.md).

## Installing the pylon Software Suite

Install the pylon software suite from Basler together with installing pypylon and required supplementary packages, e.g. for 3D cameras.
Note: The pypylon wheel package already includes the [pylon C++ runtimes](pylon-software-suite.md#sdk-and-apis) and [vTools](vtools.md). This is sufficient for using pypylon and works immediately for transport layers that don't require any extra drivers.

You can download the [pylon Software Suite](pylon-software-suite.md) as well as any additional supplementary packages, e.g., for 3D cameras, from the [Basler website](https://www.baslerweb.com/en/downloads/software/?downloadCategory.values.label.data=pylon) if required.

The installation wizard of the pylon Software Suite guides you through the process and allows you to decide which components to install. The following components are recommended:

- USB/GigE drivers
- CXP GenTL producer and drivers (if using CXP cameras)
- pylon Viewer

## Installing pypylon

pypylon is available from [PyPi](https://pypi.org/project/pypylon/). To install it, run the following command:

```Shell
pip install pypylon
```

When you run _pip install_ on some systems, you may see something like this:
`error: externally-managed-environment
× This environment is externally managed
To install Python packages system-wide, use your system package manager, for instance on Ubuntu23.04+.`
This means your OS manages that Python installation.
It helps prevent pip from changing system packages.

### Alternative 1 Virtual environment (recommended)
Python “Virtual Environments” allow Python packages to be installed in an isolated
location for a particular application, rather than being installed globally. Using
venv install in folder _DIR_ you need to perform following steps:
```Shell
python3 -m venv <DIR>
source <DIR>/bin/activate # MacOS/ Linux
<DIR>\Scripts\activate    # Windows
pip install pypylon
deactivate
```
This works identically inside Docker, WSL, Raspberry Pi, and Conda setups. Each project gets its own dependency tree, and upgrades in one project never affect another.

### Alternative 2 System-wide Installation
`sudo python3 -m pip install pypylon --break-system-packages`
This approach is rather simple and the module is available to all user immediately.
Besides requiring root privileges it brings further draw-backs.
1. It can conflict with Debian package management.
2. Future Debian or Python updates may break things.

Generally this is discouraged on modern Debian systems.

## Verify Installation
To verify the pypylon installation, run the following command:

```Shell
source <DIR>/bin/activate # MacOS/ Linux
<DIR>\Scripts\activate    # Windows
```
```Python
from pypylon import pylon

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()

print("Detected:", len(devices))
```

## GigE Optimization

If you're planning to use GigE cameras, the following optimizations are recommended:

- Use a dedicated network interface card (NIC)
- Enable jumbo frames (MTU 9000)
- Disable energy saving

## Distributing pypylon
Pypylon provides a complete pylon Runtime, so it is not required to install pylon Software Suite.
In case you also require camera, or frame grabber driver take a look in [pylon Deployment Guide](https://docs.baslerweb.com/pylonapi/pylon-deployment-guide.html) .
