#!/usr/bin/env python
from setuptools import setup, Extension
from setuptools.command.build_ext import new_compiler

import argparse
import ctypes
import datetime
import glob
import stat
import os
import re
import shutil
import subprocess
import sys
import platform
from pathlib import Path
from logging import info, warning, error
# The pylon version this source tree was designed for, by platform
ReferencePylonVersion = {
    "Windows": "10.2.1",
    # ATTENTION: This version is the pylon core version reported by pylon-config,
    # which is not equal to the version on the outer tar.gz
    "Linux": "10.0.2",
    "Linux_armv7l": "6.2.0",
    "Darwin": "10.0.2"
}

################################################################################

def prepare_for_limited_api(min_ver_str):
    min_maj, min_min = map(int, min_ver_str.split("."))
    py_ver_too_low = sys.version_info[:2] < (min_maj, min_min)
    # Disable limited api when python version is to low
    if py_ver_too_low:
        return None, None
    return f"0x{min_maj:02x}{min_min:02x}0000", f"cp{min_maj}{min_min}"

MIN_PY_VER_FOR_LIMITED_API = "3.9" # some low value to prove that it works
LIMIT_DEF, LIMIT_TAG = prepare_for_limited_api(MIN_PY_VER_FOR_LIMITED_API)

################################################################################

def get_machinewidth():
    # From the documentation of 'platform.architecture()':
    #   "Note:
    #    On Mac OS X (and perhaps other platforms), executable files may be
    #    universal files containing multiple architectures. To get at the
    #    '64-bitness# of the current interpreter, it is more reliable to query
    #    the sys.maxsize attribute.
    #   "
    if sys.maxsize > 2147483647:
        return 64
    else:
        return 32

def get_platform():
    return platform.system()

def get_machine():
    if get_platform() == "Darwin" and "ARCHFLAGS" in os.environ:
        # crossbuild settings: ARCHFLAGS="-arch arm64" or ARCHFLAGS="-arch x86_64"
        return os.environ["ARCHFLAGS"].split()[1]
    else:
        return platform.machine()

def rxglob(path, pattern, recursive=False):
    if isinstance(pattern, str):
        if not pattern.endswith("$"):
            pattern += "$"
        pattern = re.compile(pattern)
    for entry in Path(path).iterdir():
        if pattern.match(entry.name):
            yield entry
        if recursive and entry.is_dir():
            yield from rxglob(entry, pattern, recursive)

class BuildSupport(object):

    # --- Constants ---

    # Mapping from python platform to pylon platform dirname
    BinPath = {
        ('Windows', 32): 'Win32',
        ('Windows', 64): 'x64',
        ('Linux', 32): 'lib',
        ('Linux', 64): 'lib64',
        ('Darwin', 64): 'lib64'
        } [ (get_platform(), get_machinewidth()) ]

    # Compatible swig versions
    SwigVersions = ["4.2.0", "4.2.1"]
    SwigOptions = [
        "-c++",
        "-Wextra",
        "-Wall",
        "-threads",
        #lots of debug output "-debug-tmsearch",
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
        "pylondataprocessing",
        }

    # Global switch to toggle pylon data processing support on or off
    # If set to true the pylon used for building must support at least pylon data processing 1.3 (pylon 7.4+)
    IncludePylonDataProcessing = True

    # --- Attributes to be set by init (may be platform specific) ---

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

    def dump(self):
        for a in dir(self):
            info("%s=%s" % (a, getattr(self, a)))

    def find_swig(self):
        # Find SWIG executable
        swig_executable = None
        # swig from pypi
        try:
            import swig
            swig_executable = os.path.join(swig.BIN_DIR, "swig")
        except ModuleNotFoundError:
            # swig from path
            swig_executable = shutil.which("swig")

        if swig_executable and self.is_supported_swig_version(swig_executable):
            info("Found swig: %s" % (swig_executable,))
            return swig_executable
        else:
            raise RuntimeError("swig executable not found on path!")

    def is_supported_swig_version(self, swig_executable):
        if swig_executable is None:
            return False

        try:
            output = subprocess.check_output(
                [swig_executable, "-version"],
                universal_newlines=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

        res = re.search(r"SWIG Version ([\d\.]+)", output)
        if res is None:
            return False

        if tuple(map(int, res.group(1).split('.'))) < (4, 2, 0):
            msg = (
                "The version of swig is %s which is too old. " +
                "Minimum required version is 4.2.0"
                )
            warning(msg, res.group(1))
            return False

        return True


    def call_swig(self, sourcedir, source, version, skip=False):
        name = os.path.splitext(source)[0]
        cpp_name = os.path.abspath(
            os.path.join(self.GeneratedDir, "%s_wrap.cpp" % name)
            )

        if skip:
            return cpp_name

        outdir = os.path.abspath(self.PackageDir)

        for inc in self.get_swig_includes():
            self.SwigOptions.append("-I%s" % inc)

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
        package_dir = os.path.abspath(self.PackageDir)
        for package in self.get_deploy_list():
            for src, dst in self.RuntimeFiles[package]:
                dst = os.path.join(package_dir, dst)
                if not os.path.exists(dst):
                    os.makedirs(dst)
                src = os.path.join(runtime_dir, src)
                for f in glob.glob(src):
                    print("Copy %s => %s" % (f, dst))
                    shutil.copy(f, dst)
            if package in self.RuntimeFolders:
                for src, dst, ignorepatterns in self.RuntimeFolders[package]:
                    dst = os.path.join(package_dir, dst)
                    src = os.path.join(runtime_dir, src)
                    shutil.rmtree(dst, ignore_errors=True)
                    print("Copy tree %s => %s (ignoring=%s)" % (src, dst, str(ignorepatterns)))
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignorepatterns))


    def clean(self, mode, additional_dirs=None):
        if mode == 'skip':
            return
        clean_dirs = [self.GeneratedDir, self.PackageDir]
        if additional_dirs:
            clean_dirs.extend(additional_dirs)
        for cdir in clean_dirs:
            print("Remove:", cdir)
            shutil.rmtree(cdir, ignore_errors=True)
        if mode == 'keep':
            os.makedirs(self.GeneratedDir)
            os.makedirs(self.PackageDir)


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
            m_rel = re.match(
                r"^\d+(?:\.\d+){2,3}(?:(?:a|b|rc)\d*)?$",
                git_version
                )
            #this will match  something like 1.0.0-14-g123456 and
            # 1.0.0-14-g123456-dirty and 1.0.0-dirty
            rx_git_ver = re.compile(
                r"""
                ^(\d+(?:\.\d+){2,3}
                (?:(?:a|b|rc)\d*)?)
                (?:(?:\+[a-zA-Z0-9](?:[a-zA-Z0-9\.]*[a-zA-Z0-9]?))?)
                (?:-(\d+)-g[0-9a-f]+)?
                (?:-dirty)?$
                """,
                re.VERBOSE
                )
            m_dev = rx_git_ver.match(git_version)
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
            return "%d.%d.%d.dev0" % (
                now.year,
                now.month,
                now.day
            )

    def get_version(self):
        git_version = self.get_git_version()
        pylon_version = self.get_pylon_version()

        #strip the build number from the pylon version
        #on linux an optional tag might be included in the version
        match = re.match(r"^(\d+\.\d+\.\d+)\.\d+(.*)", pylon_version)
        pylon_version_no_build = match.group(1)
        pylon_version_tag = match.group(2)

        reference_version = ReferencePylonVersion[get_platform()]

        # check for a more specialized reference version
        platform_machine = get_platform() + "_" + get_machine()
        if platform_machine in ReferencePylonVersion:
            reference_version = ReferencePylonVersion[platform_machine]

        if (
            pylon_version_no_build == reference_version and
            pylon_version_tag == ''
            ):
            pypylon_version = git_version
        else:
            # Build is against a non-reference version of pylon.
            # Se we add that info to the pypylon version.

            # Remove all characters forbidden in a local version
            # (- and _ get normalized anyways)
            pylon_version_tag_cleaned=re.sub(
                r"[^a-zA-Z0-9\.-_]",
                '',
                pylon_version_tag
                )
            pypylon_version = "%s+pylon%s%s" % (
                git_version,
                pylon_version_no_build,
                pylon_version_tag_cleaned
                )
            warning("pylon version differs from the reference version (got: %s, expected: %s)" % (pylon_version_no_build, reference_version))

        return pypylon_version

    def get_short_version(self, version):
        return version.split('+')[0]

    @staticmethod
    def make():
        if get_platform() == "Windows":
            return BuildSupportWindows()
        elif get_platform() == "Linux":
            return BuildSupportLinux()
        elif get_platform() == "Darwin":
            return BuildSupportMacOS()
        else:
            error("Unsupported platform")

    def get_package_data_files(self):
        # patterns for files in self.PackageDir
        data_files = ["*.dll", "*.zip", "*.so", "*.so.*", "*.sig"]

        # also add all files of any sub-directories recursively
        pdir = self.PackageDir
        for entry in os.listdir(self.PackageDir):
            jentry = os.path.join(pdir, entry)
            if stat.S_ISDIR(os.stat(jentry).st_mode):
                for (root, _, fnames) in os.walk(jentry):
                    for fname in fnames:
                        # file names have to be relative to self.PackageDir
                        jname = os.path.join(root, fname)
                        pdir_rel = os.path.relpath(jname, self.PackageDir)
                        data_files.append(pdir_rel)

        return data_files

    def get_pylon_version_tuple(self):
        parts = self.get_pylon_version().split(".")
        # parts[3] (patchlevel) might contain non numeric characters. We just
        # take the leading numerals.
        parts[3] = re.search(r'\d+', parts[3]).group()
        return tuple(map(int, parts))


    def include_pylon_data_processing(self):
        # pylon Versions since 7.0 support data processing but the pypylon mapping has been introduced with 7.4.
        # previous pylon versions are missing required header files used by pypylon
        result = self.IncludePylonDataProcessing and self.get_pylon_version_tuple() >= (7, 4, 0, 0)
        return result

    def get_deploy_list(self):
        if self.include_pylon_data_processing():
            return self.RuntimeDefaultDeploy
        else:
            result = self.RuntimeDefaultDeploy.copy()
            result.remove("pylondataprocessing")
            return result

################################################################################

class BuildSupportWindows(BuildSupport):

    # Base directory for pylon SDK on Windows
    PylonDevDir = None

    RuntimeFiles = {

        "base": [
            ("PylonBase_*.dll", ""),
            ("GCBase_MD_*.dll", ""),
            ("GenApi_MD_*.dll", ""),
            ("log4cpp_MD_*.dll", ""),
            ("Log_MD_*.dll", ""),
            ("NodeMapData_MD_*.dll", ""),
            ("XmlParser_MD_*.dll", ""),
            ("MathParser_MD_*.dll", ""),
            ],

        "gige": [
            ("PylonGigE_*.dll", ""),
            ("gxapi*.dll", ""),
            ],

        "usb": [
            ("PylonUsb_*.dll", ""),
            ("uxapi*.dll", ""),
            ],

        "camemu": [
            ("PylonCamEmu_*.dll", ""),
            ],

        "extra": [
            ("PylonGUI_*.dll", ""),
            ("PylonUtility_*.dll", ""),
            ("PylonUtilityPcl_*.dll", ""),
            ],

        "pylondataprocessing": [
            ("PylonDataProcessing_v*.dll", ""),
            ("PylonDataProcessing_v*.sig", ""),
            ("PylonDataProcessingCore_*.dll", ""),
            ],

        "gentl": [
            ("PylonGtc_*.dll", ""),
            ],
        }

    PYLON_DATA_PROCESSING_VTOOLS_DIR = "pylonDataProcessingPlugins"
    PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR = "DataProcessingPluginsB"

    RuntimeFolders = {
        "pylondataprocessing": [
            (PYLON_DATA_PROCESSING_VTOOLS_DIR, PYLON_DATA_PROCESSING_VTOOLS_DIR, ("*Editor*.dll",)),
            (PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR, PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR, ()),
            ],
        }

    DefineMacros = [
        ("UNICODE", None),
        ("_UNICODE", None),
        ("_CRT_SECURE_NO_WARNINGS", None),

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

    def _detect_msvc_ver(self):
        stderr = b""
        try:
            msvc = new_compiler(compiler='msvc')
            msvc.initialize()
            kw = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
            with subprocess.Popen([msvc.cc], **kw) as process:
                _, stderr = process.communicate()
        except Exception:
            pass
        stderr = stderr.decode("ascii", errors="backslashreplace")
        m = re.search(r"\s+(\d+(?:\.\d+)+)\s+", stderr)
        return tuple(map(int, m.group(1).split('.'))) if m else (16, 0)

    def __init__(self):
        super(BuildSupportWindows, self).__init__()
        self.SwigExe = self.find_swig()
        self.SwigOptions.append("-DHAVE_PYLON_GUI")
        self.SwigOptions.append("-D_WIN32")
        if get_machinewidth() != 32:
            self.SwigOptions.append("-D_WIN64")

        self.PylonDevDir = os.environ.get("PYLON_DEV_DIR")
        if not self.PylonDevDir:
            # Fallback, try to locate pylon installation via registry key
            import winreg
            try:
                # Read install location from registry entry
                basler_pylon_registry_key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Basler\pylon')
                basler_pylon_install_folder = winreg.QueryValueEx(basler_pylon_registry_key, "InstallationFolder")[0]

                # Check if install folder contain "Development" folder.
                basler_pylon_install_dev_dir = os.path.join(basler_pylon_install_folder, "Development")
                if os.path.exists(basler_pylon_install_dev_dir):
                    self.PylonDevDir = basler_pylon_install_dev_dir

            except OSError as error:
                print("Fallback, locate of pylon installation via registry failed:", error)

            # Throw exception if registry fallback failed.
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

        self.msvc_ver = self._detect_msvc_ver()

        if self.msvc_ver >= (19, 13):
            # add '/permissive-' to detect skipping initialization with goto
            # (available since VS 2017)
            self.ExtraCompileArgs.append('/permissive-')

    def get_swig_includes(self):
        return [os.path.join(self.PylonDevDir, "include")]

    def use_debug_configuration(self):
        self.ExtraCompileArgs.append('/Od')     # disable optimizations
        self.ExtraCompileArgs.append('/Zi')     # create debug info
        self.ExtraLinkArgs.append('/DEBUG')     # create pdb file

    def find_swig(self):
        #this searches for swigwin-<version>\swig.exe at the usual places
        env_names = ['PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432']
        search = [os.environ[n] for n in env_names if n in os.environ]

        for prg in search:
            for swig_version in self.SwigVersions:
                candidate = os.path.join(
                    prg,
                    "swigwin-%s" % swig_version,
                    "swig.exe"
                    )
                if self.is_supported_swig_version(candidate):
                    info("Found swig: %s" % (candidate,))
                    return candidate

        #fallback to the standard implementation
        return BuildSupport.find_swig(self)

    def copy_runtime(self):
        super(BuildSupportWindows, self).copy_runtime()

        # detect OS and target bitness
        os_bits = 64
        if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
            # might be WOW
            wow = os.environ.get('PROCESSOR_ARCHITEW6432', False)
            if not wow:
                os_bits = 32
        tgt_bits = get_machinewidth()

        # Copy msvc runtime for pylon
        runtime_dlls = ["vcruntime140.dll", "msvcp140.dll"]
        if tgt_bits == 64 and self.msvc_ver >= (19, 20):
            runtime_dlls.append("vcruntime140_1.dll")
        sysname = "System32" if tgt_bits == 64 or os_bits == 32 else "SysWOW64"
        sysdir = os.path.join(os.environ["windir"], sysname)
        for dll in runtime_dlls:
            src = os.path.join(sysdir, dll)
            print("Copy %s => %s" % (src, self.PackageDir))
            shutil.copy(src, self.PackageDir)

    def get_pylon_version(self):
        dll_dir = os.path.realpath(
            os.path.join(
                self.PylonDevDir,
                "..",
                "Runtime",
                self.BinPath
                )
            )
        dll_pattern = os.path.join(dll_dir, "PylonBase_*.dll")
        lst = glob.glob(dll_pattern)
        if lst:
            dll_path = lst[0]
        else:
            raise EnvironmentError("could not find PylonBase")

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
        os.getenv('PYLON_ROOT', '/opt/pylon'),
        'bin/pylon-config'
        )

    PylonDataProcessingConfig = os.path.join(
        os.getenv('PYLON_ROOT', '/opt/pylon'),
        'bin/pylon-dataprocessing-config'
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

    # N.B.: For libraries pylons library folder does not just contain an shared
    #       object file but also symlinks that refer to that shared object (
    #       possibly through a cascade of several links).
    #       When pypylon links to these libraries, the linker will follow the
    #       first symlink and will record the target of that link as a
    #       dependency in the pypylon binary. Since the copy operations that are
    #       necessary to build pypylon follow symlinks, the result of these
    #       copy operations - in the presence of symlinks - would be that we
    #       get several copies of the shared object, which of course is
    #       undesirable.
    #       So we have to ensure that the following patterns include at least
    #       the shared object itself. If there is no or only one symlink for
    #       this file, nothing more is needed. This is the case for all pylon
    #       versions up to 6.3.0.18933. Later versions use up to two symlinks
    #       and in that case we have to copy the second symlink with
    #       'follow_symlinks=True' so that we get the contents of the shared
    #       object and the name of the dependency that was recorded in the
    #       pypylon binary.
    #       In addition to the change in the number of symlinks there was also
    #       a change in the naming scheme:
    #        - old: <basename>-<dotted-version>.so
    #        - new: <basename>.so.<dotted-version>, no more version numbers in
    #          TL libraries
    #
    #       While it was sufficent to use glob patterns in the past, this does
    #       not work for the new naming scheme anymore - there simply is no glob
    #       pattern that matches <basename>.so.<major>.<minor> but NOT
    #       <basename>.so.<major>.<minor>.<subminor>. Therefore we have to
    #       switch to using 'real' regular expressions.

    # no differences between versions, no symlinks involved
    RuntimeFiles = {
        "base": [
            (r"libGCBase_.*\.so", ""),
            (r"libGenApi_.*\.so", ""),
            (r"liblog4cpp_.*\.so", ""),
            (r"libLog_.*\.so", ""),
            (r"libNodeMapData_.*\.so", ""),
            (r"libXmlParser_.*\.so", ""),
            (r"libMathParser_.*\.so", ""),
            ],
        "usb": [
            (r"pylon-libusb-.*\.so", ""),
            ],
        }

    # up to one symlink per library -> match shared objects only
    RuntimeFiles_up_to_6_3_0_18933 = {
        "base": [
            (r"libpylonbase-.*\.so", ""),
            ],
        "gige" : [
            (r"libpylon_TL_gige-.*\.so", ""),
            (r"libgxapi-.*\.so", ""),
            ],
        "usb": [
            (r"libpylon_TL_usb-.*\.so", ""),
            (r"libuxapi-.*\.so", ""),
            ],
        "camemu": [
            (r"libpylon_TL_camemu-.*\.so", ""),
            ],
        "extra": [
            (r"libpylonutility-.*\.so", ""),
            ],
        "gentl": [
            (r"libpylon_TL_gtc-.*\.so", ""),
            ],
        }

    # match those shared objects without symlinks directly and where there are
    # symlinks, match the second one (*.so.<major>.<minor>)
    RuntimeFiles_after_6_3_0_18933 = {
        "base": [
            (r"libpylonbase\.so\.\d+\.\d+", ""),
            ],
        "gige": [
            (r"libpylon_TL_gige\.so", ""),
            (r"libgxapi\.so\.\d+\.\d+", "")
            ],
        "usb": [
            (r"libpylon_TL_usb\.so", ""),
            (r"libuxapi\.so\.\d+\.\d+", ""),
            ],
        "camemu": [
            (r"libpylon_TL_camemu\.so", "")
            ],
        "extra": [
            (r"libpylonutility\.so\.\d+\.\d+", ""),
            (r"libpylonutilitypcl\.so\.\d+\.\d+", ""),
            ],
        "gentl": [
            (r"libpylon_TL_gtc\.so", ""),
            ],
        "pylondataprocessing": [
            (r"libPylonDataProcessing\.so\.\d+", ""),
            (r"libPylonDataProcessing.sig", ""),
            (r"libPylonDataProcessingCore\.so\.\d+", ""),
            ],
        }

    # match those shared objects without symlinks directly and where there are
    # symlinks, match the first one (*.so.<major>)
    RuntimeFiles_starting_9_0_3_215 = {
        "base": [
            (r"libpylonbase\.so\.\d+", ""),
            ],
        "gige": [
            (r"libpylon_TL_gige\.so", ""),
            (r"libgxapi\.so\.\d+", "")
            ],
        "usb": [
            (r"libpylon_TL_usb\.so", ""),
            (r"libuxapi\.so\.\d+", ""),
            ],
        "camemu": [
            (r"libpylon_TL_camemu\.so", "")
            ],
        "extra": [
            (r"libpylonutility\.so\.\d+", ""),
            (r"libpylonutilitypcl\.so\.\d+", ""),
            ],
        "gentl": [
            (r"libpylon_TL_gtc\.so", ""),
            ],
        "pylondataprocessing": [
            (r"libPylonDataProcessing\.so\.\d+", ""),
            (r"libPylonDataProcessing.sig", ""),
            (r"libPylonDataProcessingCore\.so\.\d+", ""),
            ],
        }
    PYLON_DATA_PROCESSING_VTOOLS_DIR = "pylondataprocessingplugins"
    PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR = "dataprocessingpluginsb"

    RuntimeFolders = {
        "pylondataprocessing": [
            (PYLON_DATA_PROCESSING_VTOOLS_DIR, PYLON_DATA_PROCESSING_VTOOLS_DIR, ("*Editor*.so",)),
            (PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR, PYLON_DATA_PROCESSING_VTOOLS_CREATOR_DIR, ()),
            ],
        }

    def __init__(self):
        super(BuildSupportLinux, self).__init__()
        self.SwigExe = self.find_swig()

        self.SwigOptions.append("-DSWIGWORDSIZE%i" % (get_machinewidth(),) )

        config_cflags = self.call_pylon_config("--cflags")
        self.ExtraCompileArgs.extend(config_cflags.split())
        if self.include_pylon_data_processing():
            config_cflags = self.call_pylon_dataprocessing_config("--cflags")
            self.ExtraCompileArgs.extend(config_cflags.split())
            self.ExtraCompileArgs = list(dict.fromkeys(self.ExtraCompileArgs)) #remove duplicates
        print("ExtraCompileArgs:", self.ExtraCompileArgs)

        config_libs = self.call_pylon_config("--libs")
        self.ExtraLinkArgs.extend(config_libs.split())
        if self.include_pylon_data_processing():
            config_libs = self.call_pylon_dataprocessing_config("--libs")
            self.ExtraLinkArgs.extend(config_libs.split())
            self.ExtraLinkArgs = list(dict.fromkeys(self.ExtraLinkArgs)) #remove duplicates
        print("ExtraLinkArgs:", self.ExtraLinkArgs)

        config_libdir = self.call_pylon_config("--libdir")
        self.LibraryDirs.extend(config_libdir.split())
        if self.include_pylon_data_processing():
            config_libdir = self.call_pylon_dataprocessing_config("--libdir")
            self.LibraryDirs.extend(config_libdir.split())
            self.LibraryDirs = list(dict.fromkeys(self.LibraryDirs)) #remove duplicates
        print("LibraryDirs:", self.LibraryDirs)

        # adjust runtime files according to pylon version
        version = self.get_pylon_version_tuple()

        if version <= (6, 3, 0, 18933):
            add_runtime = self.RuntimeFiles_up_to_6_3_0_18933
        elif (6, 3, 0, 18933) < version < (9, 0, 3, 215):
            add_runtime = self.RuntimeFiles_after_6_3_0_18933
        else:
            add_runtime = self.RuntimeFiles_starting_9_0_3_215
        for package in add_runtime:
            if package in self.RuntimeFiles:
                self.RuntimeFiles[package].extend(add_runtime[package])
            else:
                self.RuntimeFiles[package] = add_runtime[package]

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


    def get_swig_includes(self):
        # add compiler include paths to list
        includes = [i[2:] for i in self.ExtraCompileArgs if i.startswith("-I")]
        return includes

    def copy_runtime(self):
        runtime_dir = self.call_pylon_config("--libdir")
        for package in self.get_deploy_list():
            for src, dst in self.RuntimeFiles[package]:
                full_dst = os.path.abspath(os.path.join(self.PackageDir, dst))
                if not os.path.exists(full_dst):
                    os.makedirs(full_dst)

                for f in rxglob(runtime_dir, src):
                    print("Copy %s => %s" % (f, full_dst))
                    # Although 'True' is the default value for 'follow_symlinks'
                    # we set it explicitly to clarify that we depend on
                    # following symlinks.
                    shutil.copy(str(f), full_dst, follow_symlinks=True)
            if package in self.RuntimeFolders:
               for src, dst, ignorepatterns in self.RuntimeFolders[package]:
                    dst = os.path.join(self.PackageDir, dst)
                    src = os.path.join(runtime_dir, src)
                    shutil.rmtree(dst, ignore_errors=True)
                    print("Copy tree %s => %s (ignoring=%s)" % (src, dst, str(ignorepatterns)))
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignorepatterns))

    def call_pylon_config(self, *args):
        params = [self.PylonConfig]
        params.extend(args)
        try:
            res = subprocess.check_output(params, universal_newlines=True)
        except FileNotFoundError:
            msg = (
                "Couldn't find pylon. Please install pylon in /opt/pylon " +
                "or tell us the installation location using the PYLON_ROOT " +
                "env variable"
                )
            error(msg)
            raise
        return res.strip()

    def call_pylon_dataprocessing_config(self, *args):
        params = [self.PylonDataProcessingConfig]
        params.extend(args)
        try:
            res = subprocess.check_output(params, universal_newlines=True)
        except FileNotFoundError:
            msg = (
                "Couldn't find pylon. Please install pylon in /opt/pylon " +
                "or tell us the installation location using the PYLON_ROOT " +
                "env variable"
                )
            error(msg)
            raise
        return res.strip()

    def get_pylon_version(self):
        pylon_version = self.call_pylon_config("--version")

        # workaround for pylon 8.0.0 on linux
        if pylon_version == "9...":
            pylon_version = "9.0.3.215"

        return pylon_version

################################################################################


class BuildSupportMacOS(BuildSupport):

    FrameWorkPath_env = os.getenv('PYLON_FRAMEWORK_LOCATION', 'undef')

    FrameworkPath = "/Library/Frameworks" if (FrameWorkPath_env=='undef' or FrameWorkPath_env=="") else FrameWorkPath_env

    FrameworkName = 'pylon.framework'

    PylonConfig = os.path.join(
        FrameworkPath,
        FrameworkName,
        'Versions/Current/Resources/Tools/pylon-config'
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
                       '-Wno-switch',
                       '-std=c++17'
                       ]

    ExtraLinkArgs = [
                    '-g0',
                    '-Wl,-rpath,@loader_path',
                    '-Wl,-framework,pylon',
                    '-F' + FrameworkPath
                    ]

    RuntimeFolders = {}

    def __init__(self):
        super(BuildSupportMacOS, self).__init__()
        self.SwigExe = self.find_swig()

        self.SwigOptions.append("-DSWIGWORDSIZE%i" % (get_machinewidth(),) )

        includes_dir = os.path.abspath(
            os.path.join('.' , "osx_includes")
            )
        old_cwd = os.getcwd()
        if not os.path.isdir(includes_dir):
            os.makedirs(includes_dir)
        os.chdir(includes_dir)

        # simulate implicit include path as swig is unaware of frameworks
        fakeframeinclude = 'pylon'
        if (os.path.islink(fakeframeinclude)):
            os.remove(fakeframeinclude)

        os.symlink(
            os.path.join(self.FrameworkPath, self.FrameworkName, 'Headers'),
            'pylon'
            )

        os.chdir(old_cwd)
        self.ExtraCompileArgs.append("-I{}".format(includes_dir))
        self.ExtraCompileArgs.append(
            '-I' + os.path.join(
                self.FrameworkPath,
                self.FrameworkName,
                'Headers',
                'GenICam'
                )
            )

    def call_pylon_config(self, *args):
        params = [self.PylonConfig]
        params.extend(args)
        try:
            res = subprocess.check_output(params, universal_newlines=True)
        except FileNotFoundError:
            msg = (
                "Couldn't find pylon. Please install pylon in %s or tell us " +
                "the framwork search path of the pylon.framework using the PYLON_FRAMEWORK_LOCATION environment " +
                "variable"
                )
            error(msg, self.FrameworkPath)
            raise

        # work around simple shells
        badprefix='-n '
        if res.startswith(badprefix):
            res = res[len(badprefix):]

        return res.strip()

    def get_pylon_version(self):
        pylon_version = self.call_pylon_config("--version")

        # workaround for pylon 8.0.0 on macOS
        if pylon_version == "9...":
            pylon_version = "9.0.3.215"

        return pylon_version

    def get_swig_includes(self):
        # add compiler include paths to list
        includes = [i[2:] for i in self.ExtraCompileArgs if i.startswith("-I")]
        # append framework paths manually
        includes += [
            os.path.join(self.FrameworkPath, self.FrameworkName, 'Headers'),
            os.path.join(
                self.FrameworkPath,
                self.FrameworkName,
                'Headers',
                'GenICam'
                )
            ]
        return includes

    def copy_runtime(self):
        full_dst = os.path.join(
            os.path.abspath(self.PackageDir),
            self.FrameworkName
            )

        if not os.path.exists(full_dst):
            shutil.copytree(
                os.path.join(self.FrameworkPath, self.FrameworkName),
                full_dst,
                symlinks=True,
                ignore = shutil.ignore_patterns("*.h","CMake","Tools")
                )
            # cleanup double TL entries in pylon 6.2.0
            if self.get_pylon_version() == "6.2.0.18677":
                for p in Path(f"{full_dst}").glob("**/*TL*.so"):
                    if re.match(r".*TL_[a-z]+\.so", p.name):
                        info(f"DELETE {p}")
                        os.remove(p)
            # Patch minimum required OS version for pylon 10.0.2 or newer for external provided libusb
            if self.get_pylon_version() >= "10.0.2.471":
                import lief
                import tempfile
                # Create a temp directory
                temp_dir = tempfile.mkdtemp()
                # Patch and write per-arch files
                for p in Path(f"{full_dst}").glob("**/pylon-libusb-1.0.27.dylib"):
                    fat_binary = lief.MachO.parse(str(p))
                    for binary in fat_binary:
                        info(f"Patching architecture: {binary.header.cpu_type} - {binary.header.cpu_subtype}")
                        for command in binary.commands:
                            if isinstance(command, lief.MachO.BuildVersion):
                                command.minos = (14, 0, 0)  # Set macOS 14.0 as minimum version
                                command.sdk = (14, 0, 0)  # Set macOS SDK 14.0 as minimum version
                        output_path = os.path.join(temp_dir, f"pylon-libusb-1.0.27-{binary.header.cpu_type.name}.dylib")
                        binary.write(output_path)
                    # Recombine into a universal binary
                    fat_binary.write(str(p))
                    # Repair/replace signature of patched libusb
                    info("Create AdHoc signature for \"" +  os.path.basename(str(p)) +  "\"...")
                    subprocess.run(["codesign", "--force", "-s", "-", str(p)], check=True)
                # Repair/replace signature of pylon.framework
                info("Create AdHoc signature for \"" +  os.path.basename(full_dst) + "\"...")
                subprocess.run(["codesign", "--force", "-s", "-", full_dst], check=True)

    def include_pylon_data_processing(self):
        return False

################################################################################
################################################################################
################################################################################

if __name__ == "__main__":

    # Get a build support
    bs = BuildSupport.make()
    bs.dump()

    # Determine if we have pylon data processing available on platform
    includePylonDataProcessing = bs.include_pylon_data_processing()

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
        help="skip swig to allow patching code after SWIG generated it."
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
        bs.clean("std", ["build", "pypylon.egg-info", "dist"])
        sys.exit(0)

    if not help_mode:
        if args.rebuild_doxygen:
            print("Rebuilding DoxyGenApi.i and DoxyPylon.i")
            subprocess.call("python scripts/builddoxy2swig/builddoxygen.py")

    if not help_mode:
        print("Building version:", version)

    # Call swig for genicam and pylon extensions
    if not help_mode:

        # start with fresh 'pypylon' and 'generated' dirs if not skipping swig
        bs.clean("skip" if args.skip_swig else "keep")

        if LIMIT_DEF:
            bs.DefineMacros.append(("Py_LIMITED_API", LIMIT_DEF))

        genicam_wrapper_src = bs.call_swig(
            "src/genicam",
            "genicam.i",
            version,
            args.skip_swig
            )
        print('\n')
        pylon_wrapper_src = bs.call_swig(
            "src/pylon",
            "pylon.i",
            version,
            args.skip_swig
            )
        print('\n')
        if includePylonDataProcessing:
            pylondataprocessing_wrapper_src = bs.call_swig(
                "src/pylondataprocessing",
                "pylondataprocessing.i",
                version,
                args.skip_swig
                )
            print('\n')

        if args.swig_only:
            print("Stopping after swig...")
            sys.exit(0)

        # copy_runtime is responsible for putting all those files and directories
        # into the package directory, that need to be distributed and were not
        # placed there by 'call_swig'.
        bs.copy_runtime()
        print('\n')

    else:
        # mock to allow calling "--help" on setup
        genicam_wrapper_src, pylon_wrapper_src, pylondataprocessing_wrapper_src = "", "", ""

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
        py_limited_api=bool(LIMIT_DEF),
        )
    print('\n')
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
        py_limited_api=bool(LIMIT_DEF),
        )
    print('\n')
    if includePylonDataProcessing:
        pylondataprocessing_ext = Extension(
            'pypylon._pylondataprocessing',
            [pylondataprocessing_wrapper_src],
            include_dirs=[
                os.path.join(".", "src"), # for PyPortImpl.h
                ],
            library_dirs=bs.LibraryDirs,
            define_macros=bs.DefineMacros,
            extra_compile_args=bs.ExtraCompileArgs,
            extra_link_args=bs.ExtraLinkArgs,
            py_limited_api=bool(LIMIT_DEF),
            )
        print('\n')

    with open("README.md", "r") as fh:
        long_description = fh.read()

    # While copy_runtime sets up the package directory, get_package_data_files'
    # responsibility is to express the content of that directory in a way, that
    # is understood by 'setup()'.
    package_data_files = bs.get_package_data_files()

    setup(
        name='pypylon',
        version=version,
        author="Basler AG",
        author_email="oss@baslerweb.com",
        description="The python wrapper for the Basler pylon Camera Software Suite.",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/basler/pypylon",
        ext_modules=[genicam_ext, pylon_ext, pylondataprocessing_ext] if includePylonDataProcessing else [genicam_ext, pylon_ext],
        test_suite='tests.all_emulated_tests_with_pylondataprocessing' if includePylonDataProcessing else 'tests.all_emulated_tests',
        packages=["pypylon"],
        package_data={"pypylon": package_data_files },
        license="Other/Proprietary License",
        classifiers=[
            # Proprietary license as the resulting install contains pylon which
            # is under the pylon license
            "License :: Other/Proprietary License",
            "Programming Language :: C++",
            "Operating System :: Microsoft :: Windows :: Windows 7",
            "Operating System :: Microsoft :: Windows :: Windows 8",
            "Operating System :: Microsoft :: Windows :: Windows 10",
            "Operating System :: Microsoft :: Windows :: Windows 11",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
            "Topic :: Multimedia :: Video :: Capture",
            "Topic :: Scientific/Engineering",
        ],
        options={"bdist_wheel": {"py_limited_api": LIMIT_TAG or False}}
    )

    if args.generate_python_doc:
        print("Generating doc for python API")
        subprocess.call("python scripts/generatedoc/generatedoc.py")
