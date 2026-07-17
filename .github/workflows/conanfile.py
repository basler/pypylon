import os
import json
import shutil
import fnmatch
from conan import ConanFile
from conan.tools.files import copy


class PyPylonConanConsumer(ConanFile):
    name = "pypylon"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_config": ["ANY"],
        "control_file": ["ANY"],
        "third_party_license_file": ["ANY"]
    }
    default_options = {
        "build_config": "Placeholder will be overwritten by the CI",
        "control_file": "Placeholder will be overwritten by the CI",
        "third_party_license_file": "Placeholder will be overwritten by the CI"
    }

    def layout(self):
        # Keep generated/deployed output rooted at --output-folder.
        self.folders.generators = "."

    @property
    def _platform_name(self):
        arch = str(self.settings.arch).lower()
        os_name = str(self.settings.os).lower()
        if os_name == "linux":
            if arch == "x86_64":
                platform_key = "linux_x86_64"
            elif arch == "aarch64":
                platform_key = "linux_aarch64"
            else:
                platform_key = "linux_x86_64"
        elif os_name == "windows":
            platform_key = "windows"
        elif os_name == "macos":
            platform_key = "macos"
        else:
            platform_key = "unknown"
        return platform_key

    def _dependency_by_name(self, dep_name):
        for _, dep in self.dependencies.items():
            if dep.ref.name == dep_name:
                return dep
        return None

    def requirements(self):
        # Read the configuration and control files
        config_path = str(self.options.build_config)
        with open(config_path) as f:
            config = json.load(f)

        control_path = str(self.options.control_file)
        with open(control_path) as f:
            control = json.load(f)

        # Create a mapping of package names to versions from the control file
        version_map = {pkg["name"]: pkg["version"] for pkg in control}

        # License files
        self.requires("pylon-licenses/20251125@release/potentially-public")

        # Determine platform key
        requirements = config.get(self._platform_name, {}).get("requirements", [])
        # Special-case: the control file currently lists 'pylon-vtool-package-a-sasl'
        # with a '<base>.1' build id, which corresponds to a legacy Conan 1 recipe in
        # and fails to load under Conan 2. Force it to use the same build id
        # as 'pylon-vtool-package-a', which is the Conan 2 compatible recipe.
        vtool_package_a_version = version_map.get("pylon-vtool-package-a")
        for req in requirements:
            if req == "pylon-vtool-package-a-sasl" and vtool_package_a_version:
                version = vtool_package_a_version
            else:
                version = version_map.get(req)
            if version:
                self.requires(f"{req}/{version}@release/potentially-public")
            else:
                self.requires(f"{req}/25.09@release/potentially-public")

    def generate(self):
        # Read the configuration file
        config_path = str(self.options.build_config)
        with open(config_path) as f:
            config = json.load(f)

        # Copy legal files based on the platform
        os_name = str(self.settings.os).lower()
        if os_name == "linux":
            license_path = os.path.join(self.generators_folder, "pylon", "share", "pylon", "licenses")
            os.makedirs(license_path, exist_ok=True)
            shutil.copy2(str(self.options.third_party_license_file), license_path)
            dep = self._dependency_by_name("pylon-licenses")
            if dep:
                copy(self, "**/License.txt", src=dep.package_folder, dst=license_path, keep_path=False)
        elif os_name == "windows":
            license_path = os.path.join(self.generators_folder, "pylon", "Licenses")
            os.makedirs(license_path, exist_ok=True)
            shutil.copy2(str(self.options.third_party_license_file), license_path)
            dep = self._dependency_by_name("pylon-licenses")
            if dep:
                copy(self, "**/License.txt", src=dep.package_folder, dst=license_path, keep_path=False)
        elif os_name == "macos":
            license_path = os.path.join(self.generators_folder, "pylon", "Frameworks", "pylon.framework", "Versions", "A", "Resources")
            os.makedirs(license_path, exist_ok=True)
            shutil.copy2(str(self.options.third_party_license_file), license_path)
            dep = self._dependency_by_name("pylon-licenses")
            if dep:
                copy(self, "**/License.txt", src=dep.package_folder, dst=license_path, keep_path=False)

        # Deploy selected package contents based on configured import patterns.
        imports = config.get(self._platform_name, {}).get("imports", [])
        deploy_dst = os.path.join(self.generators_folder, "pylon")
        for _, dep in self.dependencies.items():
            if dep.ref.name == "pylon-licenses":
                continue
            if any(fnmatch.fnmatchcase(dep.ref.name, pattern) for pattern in imports):
                copy(self, "*", src=dep.package_folder, dst=deploy_dst, keep_path=True)
