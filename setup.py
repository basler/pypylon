#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, Extension
from distutils.util import get_platform
from distutils import spawn
from logging import info, warning, error

import argparse
import ctypes
import datetime
import glob
import os
import re
import shutil
import subprocess
import sys

################################################################################

class BuildSupport(object):

    # --- Constants ---

    # Mapping from python platform to pylon platform dirname
    BinPath = {
        'win32': 'Win32',
        'win-amd64': 'x64',
        'linux-i686': 'lib',
        'linux-x86_64': 'lib64',
        'linux-armv7l': 'lib',
        'linux-aarch64': 'lib64'
        }[get_platform()]

    # Compatible swig versions
    SwigVersions = ["3.0.12"]
    SwigOptions = [
        "-c++",
        "-Wextra",
        "-Wall",
        "-threads",
        "-modern",
        "-DSWIG_PYTHON_LEGACY_BOOL",
        ]

    # Where to place generated code
    GeneratedDir = os.path.join(".", "generated")

    # Directory of the final package
    PackageDir = os.path.join(".", "pypylon")

    # What parts of the runtime should be deployed by default
    RuntimeDefaultDeploy = {
        "base",
        "gige",
        "usb",
        "camemu",
        "gentl",
        "extra",
        "bcon",
        "cl"
        }

    # --- Attributes to be set by init (may be platform specific ---

    # swig executable to be called
    SwigExe = None

    # Library dirs for compiling extensions
    LibraryDirs = []

    # Macro definitions for compiling extensions
    DefineMacros = []

    # Additional compiler arguments for extensions
    ExtraCompileArgs = []

    # Additional linker arguments for extensions
    ExtraLinkArgs = []

    # Runtime files needed for copy deployment
    RuntimeFiles = {}

    def get_swig_includes(self):
        raise RuntimeError("Must be implemented by platform build support!")

    def __init__(self):

        self.SwigExe = "swig"
        if sys.version_info[0] == 3:
            self.SwigOptions.append("-py3")

    def dump(self):
        for a in dir(self):
            info("%s=%s" % (a, getattr(self, a)))

    def call_swig(self, sourcedir, source, version):

        name = os.path.splitext(source)[0]
        cpp_name = os.path.abspath(
            os.path.join(self.GeneratedDir, "%s_wrap.cpp" % name)
            )

        if not os.path.exists(self.GeneratedDir):
            os.makedirs(self.GeneratedDir)

        outdir = os.path.abspath(self.PackageDir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        for inc in self.get_swig_includes():
            self.SwigOptions.append("-I%s" % inc)

        if not args.skip_swig:
            call_args = [self.SwigExe]
            call_args.extend(["-python"])
            call_args.extend(["-outdir", outdir])
            call_args.extend(["-o", cpp_name])
            call_args.extend(self.SwigOptions)
            call_args.append(source)

            print("call", " ".join(call_args))
            subprocess.check_call(call_args, cwd=os.path.abspath(sourcedir))

            # append module version property
            with open(os.path.join(outdir, "%s.py" % name), 'at') as gpf:
                gpf.write("\n__version__ = '%s'\n" % version)

            # Python needs an __init__.py inside the package directory...
            with open(os.path.join(bs.PackageDir, "__init__.py"), "a"):
                pass

        return cpp_name

    def copy_runtime(self):

        runtime_dir = os.path.join(
            self.PylonDevDir,
            "..",
            "runtime",
            self.BinPath
            )

        for package in self.RuntimeDefaultDeploy:
            for pattern in self.RuntimeFiles[package]:
                full_p = os.path.abspath(os.path.join(runtime_dir, pattern))
                for f in glob.glob(full_p):
                    print("Copy %s => %s" % (f, self.PackageDir))
                    shutil.copy(f, self.PackageDir)

    def clean(self, additional_dirs=None):
        clean_dirs = [self.GeneratedDir, self.PackageDir]
        if additional_dirs:
            clean_dirs.extend(additional_dirs)
        for cdir in clean_dirs:
            print("Remove:", cdir)
            shutil.rmtree(cdir, ignore_errors=True)

    def get_pylon_version(self):
        raise RuntimeError("Must be implemented by platform build support!")

    def use_debug_configuration(self):
        raise RuntimeError("Must be implemented by platform build support!")

    @staticmethod
    def get_git_version():
        try:
            # GIT describe as version
            git_version = subprocess.check_output(
                ["git", "describe", "--tags", "--dirty"],
                universal_newlines=True
                )
            git_version = git_version.strip()
            m_rel = re.match("^\d+(?:\.\d+){2,3}$", git_version)
            #this will match  something like v1.0.0-14-g123456 and v1.0.0-14-g123456-dirty and v1.0.0-dirty
            m_dev = re.match("(\d+(?:\.\d+){2,3})(?:-(\d+)-g[0-9a-f]+)?(?:-dirty)?", git_version)
            if m_rel:
                # release build -> return as is
                return git_version
            if m_dev:
                # development build
                return "%s.dev%s" % (m_dev.group(1), m_dev.group(2) or 0)

            warning("failed to parse git version '%s'", git_version)
            raise OSError
        except (OSError, subprocess.CalledProcessError) as e:
            warning("git not found or invalid tag found.")
            warning("-> Building version from date!")
            now = datetime.datetime.now()
            midnight = datetime.datetime(now.year, now.month, now.day)
            todays_seconds = (now - midnight).seconds
            return "%d.%d.%d.dev%d" % (now.year, now.month, now.day, todays_seconds)

    def get_version(self):
        git_version = self.get_git_version()
        pylon_version = self.get_pylon_version()
        return "%s+pylon%s" % (git_version, pylon_version)

    def get_short_version(self, version):
        return version.split('+')[0]

    @staticmethod
    def make():
        if get_platform() in ["win32", "win-amd64"]:
            return BuildSupportWindows()
        elif get_platform() in ["linux-i686", "linux-x86_64", "linux-armv7l", "linux-aarch64"]:
            return BuildSupportLinux()

################################################################################

class BuildSupportWindows(BuildSupport):

    # Base directory for pylon SDK on Windows
    PylonDevDir = None

    DefineMacros = [
        ("UNICODE", None),
        ("_UNICODE", None),

        # let swig share its type information between the 'genicam' and the
        # 'pylon' module by using the same name for the type table.
        ("SWIG_TYPE_TABLE", "pylon")
        ]

    ExtraCompileArgs = [
        '/Gy',      # separate functions for linker
        '/GL',      # enable link-time code generation
        '/EHsc',    # set execption handling model
        ]

    ExtraLinkArgs = [
        '/OPT:REF',     # eliminate unused functions
        '/OPT:ICF',     # eliminate identical COMDAT
        '/LTCG'         # link time code generation
        ]

    RuntimeFiles = {

        "base": [
            "PylonBase_MD_VC120_v5_0.dll",
            "GCBase_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "GenApi_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "log4cpp_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "Log_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "NodeMapData_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "XmlParser_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "MathParser_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            ],

        "gige": [
            "PylonGigE_MD_VC120_v5_0_TL.dll",
            "gxapi*.dll",
            ],

        "usb": [
            "PylonUsb_MD_VC120_v5_0_TL.dll",
            "uxapi*.dll",
            ],

        "camemu": [
            "PylonCamEmu_MD_VC120_V5_0_TL.dll"
            ],

        "1394": [
            "Pylon1394_MD_VC120_v5_0_TL.dll",
            "BcamError_v5_0.dll",
            "Basler_A1_A3_A6_1394.zip",
            "Basler_scout_1394.zip",
            ],

        "bcon": [
            "BconAdapterPleora.dll",
            "bxapi_MD_VC120_v5_0.dll",
            "PylonBcon_MD_VC120_V5_0_TL.dll",
            ],

        # TODO: Test CL!!!
        "cl": [
            "PylonCLSer_MD_VC120_V5_0_TL.dll",
            "CLAllSerial_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "CLProtocol_MD_VC120_v3_0_Basler_pylon_v5_0.dll",
            "CLSerCOM.dll",
            "Basler_CameraLink.zip",
            # ARGHHH => seperate subdir!!!
            # cl lives up to its bad reputation by requiring special handling
            os.path.join(
                "..",
                "CLProtocol",
                "Win64_x64" if get_platform() == 'win-amd64' else 'Win32_i86',
                "BaslerCLProtocol.dll"
                ),
            ],

        "extra": [
            "PylonGUI_MD_VC120_v5_0.dll",
            "PylonUtility_MD_VC120_v5_0.dll"
            ],

        "gentl": [
            "PylonGtc_MD_VC120_V5_0_TL.dll"
            ],
        }

    def __init__(self):
        super(BuildSupportWindows, self).__init__()
        self.SwigExe = self.find_swig()
        self.SwigOptions.append("-DHAVE_PYLON_GUI")
        self.SwigOptions.append("-D_WIN32")
        if get_platform() != "win32":
            self.SwigOptions.append("-D_WIN64")

        self.PylonDevDir = os.environ.get("PYLON_DEV_DIR")
        if not self.PylonDevDir:
            raise EnvironmentError("PYLON_DEV_DIR is not set")
        self.LibraryDirs = [
            os.path.join(
                self.PylonDevDir,
                "lib",
                self.BinPath
                )
            ]
        for inc in self.get_swig_includes():
            self.ExtraCompileArgs.append('/I%s' % inc)

    def get_swig_includes(self):
        return [os.path.join(self.PylonDevDir, "include")]

    def use_debug_configuration(self):
        self.ExtraCompileArgs.append('/Od')     # disable optimizations
        self.ExtraCompileArgs.append('/Zi')     # create debug info
        self.ExtraLinkArgs.append('/DEBUG')     # create pdb file

    def find_swig(self):
        env_names = ['PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432']
        search = [os.environ[n] for n in env_names if n in os.environ]
        for prg in search:
            for swig_version in self.SwigVersions:
                candidate = os.path.join(
                    prg,
                    "swigwin-%s" % swig_version,
                    "swig.exe"
                    )
                if os.path.exists(candidate):
                    return candidate

        error("swig executable not found!")
        return None

    def copy_runtime(self):
        super(BuildSupportWindows, self).copy_runtime()

        # detect OS and target bitness
        os_bits = 64
        if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
            # might be WOW
            wow = os.environ.get('PROCESSOR_ARCHITEW6432', False)
            if not wow:
                os_bits = 32
        tgt_bits = (32 if get_platform() == "win32" else 64)

        # Copy msvc runtime for pylon
        runtime_dlls = ["msvcr120.dll", "msvcp120.dll"]
        sysname = "System32" if tgt_bits == 64 or os_bits == 32 else "SysWOW64"
        sysdir = os.path.join(os.environ["windir"], sysname)
        for dll in runtime_dlls:
            shutil.copy(os.path.join(sysdir, dll), self.PackageDir)

        # Copy msvcp runtime for _pylon.pyd and _genicam.pyd if that is needed.
        #
        #   Prior to VS2015 / Python 3.5 the Python setup installs the
        #   redistributable package of the runtime library and that also
        #   installed the corresponding msvcp DLL that pypylon depends upon.
        #   In those cases we do not need to do anything special.
        #
        #   With the new organisation of the VS2015 runtime library things
        #   changed. Python 3.5 installs the OS update package that adds
        #   ucrtbase.dll to the system, but it does not install vcruntime140.dll
        #   and msvcp140.dll system-wide. It simply places a copy of
        #   vcruntime140.dll alongside to python.exe. So we have to supply
        #   the msvcp140.dll that pypylon can use. We do so by copying it into
        #   the pypylon directory.

        m = re.search(r"\sv\.(\d+)\s", sys.version)
        if m:
            ver = m.group(1)[:2]
            if ver == '19':
                msvcp = os.path.join(sysdir, 'msvcp140.dll')
                shutil.copy(msvcp, self.PackageDir)


    def get_pylon_version(self):
        dll_dir = os.path.realpath(
            os.path.join(
                self.PylonDevDir,
                "..",
                "Runtime",
                self.BinPath
                )
            )
        dll_path = os.path.join(dll_dir, "PylonBase_MD_VC120_v5_0.dll")

        # temporarily add dll dir to path
        prev_path = os.environ['PATH']
        os.environ['PATH'] = os.pathsep.join((dll_dir, prev_path))

        pylon_version = [ctypes.c_uint() for _ in range(4)]
        pylon_base = ctypes.CDLL(dll_path)
        pylon_base.GetPylonVersion(*list(map(ctypes.byref, pylon_version)))

        #restore path
        os.environ['PATH'] = prev_path

        return ".".join([str(v.value) for v in pylon_version])

################################################################################

class BuildSupportLinux(BuildSupport):

    PylonConfig = os.path.join(
        os.getenv('PYLON_ROOT', '/opt/pylon5'),
        'bin/pylon-config'
        )

    DefineMacros = [
        ("SWIG_TYPE_TABLE", "pylon")
        ]

    ExtraCompileArgs = [
        '-Wno-unknown-pragmas',
        '-fPIC',
        '-g0',
        '-Wall',
        '-O3',
        '-Wno-switch'
        ]

    ExtraLinkArgs = [
        '-g0',
        '-Wl,--enable-new-dtags',
        '-Wl,-rpath,$ORIGIN',
        ]


    RuntimeFiles = {

        "base": [
            ("libpylonbase-*.so", ""),
            ("libGCBase_*.so", ""),
            ("libGenApi_*.so", ""),
            ("liblog4cpp_*.so", ""),
            ("libLog_*.so", ""),
            ("libNodeMapData_*.so", ""),
            ("libXmlParser_*.so", ""),
            ("libMathParser_*.so", ""),
            ],

        "gige": [
            ("libpylon_TL_gige-*.so", ""),
            ("libgxapi-*.so", ""),
            ],

        "usb": [
            ("libpylon_TL_usb-*.so", ""),
            ("libuxapi-*.so", ""),
            ("pylon-libusb-*.so", ""),
            ],

        "camemu": [
            ("libpylon_TL_camemu-*.so", ""),
            ],

        "1394": [], # N/A

        "bcon": [
            ("libbxapi*.so", ""),
            ("libpylon_TL_bcon-*.so", ""),
            ],

        "cl": [], # N/A

        "extra": [
            ("libpylonutility-*.so", ""),
            ],

        "gentl": [
            ("libpylon_TL_gtc*.so", ""),
            ],
        }

    def __init__(self):
        super(BuildSupportLinux, self).__init__()
        self.SwigExe = self.find_swig()
        config_cflags = self.call_pylon_config("--cflags")
        self.ExtraCompileArgs.extend(config_cflags.split())
        print("ExtraCompileArgs:", self.ExtraCompileArgs)
        config_libs = self.call_pylon_config("--libs")
        self.ExtraLinkArgs.extend(config_libs.split())
        print("ExtraLinkArgs:", self.ExtraLinkArgs)


        config_libdir = self.call_pylon_config("--libdir")
        self.LibraryDirs.extend(config_libdir.split())
        print("LibraryDirs:", self.LibraryDirs)

    def use_debug_configuration(self):
        try:
            self.ExtraCompileArgs.remove('-O3')
        except ValueError:
            pass
        try:
            self.ExtraCompileArgs.remove('-g0')
        except ValueError:
            pass
        try:
            self.ExtraLinkArgs.remove('-g0')
        except ValueError:
            pass
        self.ExtraCompileArgs.append('-O0')
        self.ExtraCompileArgs.append('-g3')
        self.ExtraLinkArgs.append('-g3')

    def find_swig(self):
        # Find SWIG executable
        swig_executable = None
        for candidate in ["swig3.0", "swig"]:
            swig_executable = spawn.find_executable(candidate)
            if swig_executable is not None:
                return swig_executable

        raise RuntimeError("swig executable not found!")

    def get_swig_includes(self):
        # add compiler include paths to list
        includes = [i[2:] for i in self.ExtraCompileArgs if i.startswith("-I")]
        return includes

    def copy_runtime(self):
        runtime_dir = self.call_pylon_config("--libdir")
        for package in self.RuntimeDefaultDeploy:
            for src, dst in self.RuntimeFiles[package]:
                full_dst = os.path.abspath(os.path.join(self.PackageDir, dst))
                if not os.path.exists(full_dst):
                    os.makedirs(full_dst)

                src = os.path.join(runtime_dir, src)
                for f in glob.glob(src):
                    print("Copy %s => %s" % (f, full_dst))
                    shutil.copy(f, full_dst)

    def call_pylon_config(self, *args):
        params = [self.PylonConfig]
        params.extend(args)
        res = subprocess.check_output(params, universal_newlines=True)
        return res.strip()

    def get_pylon_version(self):
        return self.call_pylon_config("--version")

################################################################################
################################################################################
################################################################################

if __name__ == "__main__":

    # Get a build support
    bs = BuildSupport.make()
    bs.dump()

    # Parse command line for extra arguments
    parser = argparse.ArgumentParser(
        description="Build pypylon",
        add_help=False
        )
    parser.add_argument(
        "--pp-version",
        default=bs.get_version(),
        help="set version of packages (normally set by GIT info)"
        )
    parser.add_argument(
        "--pp-debug",
        action='store_true',
        help="build debug configuration"
        )
    parser.add_argument(
        "--swig-only",
        action='store_true',
        help="exit after swig generation"
        )
    parser.add_argument(
        "--skip-swig",
        action='store_true',
        help="skip swig to allow compiling code that was patched after SWIG generated it."
        )
    parser.add_argument(
        "--rebuild-doxygen",
        action='store_true',
        help="rebuild DoxyGenApi.i and DoxyPylon.i from PYLON_DEV_DIR"
        )
    parser.add_argument(
        "--generate-python-doc",
        action='store_true',
        help="generate python doc for pypylon"
        )
    args, remainder = parser.parse_known_args()

    # re-build argv so that setup likes it...
    progname = sys.argv[0]
    sys.argv = [progname] + remainder

    # Check if help is requested...
    help_mode = False
    if "-h" in remainder or "--help" in remainder:
        help_mode = True
        parser.print_help()

    if args.pp_debug:
        bs.use_debug_configuration()
        args.pp_version += '_dbg'
    version = args.pp_version

    if "clean" in remainder:
        # Remove everything, including the "build" dir from setuptools
        print("Cleaning...")
        bs.clean(["build", "pypylon.egg-info"])
        sys.exit(0)

    if not help_mode:
        if args.rebuild_doxygen:
            print("Rebuilding DoxyGenApi.i and DoxyPylon.i")
            subprocess.call("python scripts/builddoxy2swig/builddoxygen.py")

    if not help_mode:
        print("Building version:", version)

    # Call swig for genicam and pylon extensions
    if not help_mode:
        genicam_wrapper_src = bs.call_swig(
            "src/genicam",
            "genicam.i",
            version
            )
        pylon_wrapper_src = bs.call_swig(
            "src/pylon",
            "pylon.i",
            version
            )

        if args.swig_only:
            print("Stopping after swig...")
            sys.exit(0)

        # Copy the runtime DLLs
        bs.copy_runtime()

    else:
        # mock to allow calling "--help" on setup
        genicam_wrapper_src, pylon_wrapper_src = "", ""

    # Define extensions
    genicam_ext = Extension(
        'pypylon._genicam',
        [genicam_wrapper_src],
        include_dirs=[
            os.path.join(".", "src", "genicam") # for PyPortImpl.h
            ],
        library_dirs=bs.LibraryDirs,
        define_macros=bs.DefineMacros,
        extra_compile_args=bs.ExtraCompileArgs,
        extra_link_args=bs.ExtraLinkArgs,
        )

    pylon_ext = Extension(
        'pypylon._pylon',
        [pylon_wrapper_src],
        include_dirs=[
            os.path.join(".", "src"), # for PyPortImpl.h
            ],
        library_dirs=bs.LibraryDirs,
        define_macros=bs.DefineMacros,
        extra_compile_args=bs.ExtraCompileArgs,
        extra_link_args=bs.ExtraLinkArgs,
        )

    # Now everything is in place to call setup...
    #we must not use package_dir to allow develop installs
    setup(
        name='pypylon',
        version=version,
        ext_modules=[genicam_ext, pylon_ext],
        test_suite='tests.all_emulated_tests',
        packages=["pypylon"],
        package_data={
            "pypylon": ["*.dll", "*.zip", "*.so"]
            }
        )

    if args.generate_python_doc:
        print("Generating doc for python API")
        subprocess.call("python scripts/generatedoc/generatedoc.py")
