import json
from conan import ConanFile


class PyPylonConanConsumer(ConanFile):
    name = "pypylon"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_config": ["ANY"],
        "control_file": ["ANY"]
    }
    default_options = {
        "build_config": ".github/workflows/build_config.json",
        "control_file": ".github/workflows/control_file_dummy.json"
    }

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

        # Determine platform key
        requirements = config.get(self._platform_name, {}).get("requirements", [])
        for req in requirements:
            version = version_map.get(req)
            if version:
                self.requires(f"{req}/{version}@release/potentially-public")
            else:
                self.requires(f"{req}/25.09@release/potentially-public")

    def imports(self):
        # Read the configuration file
        config_path = str(self.options.build_config)
        with open(config_path) as f:
            config = json.load(f)

        # Copy the imports based on the platform
        imports = config.get(self._platform_name, {}).get("imports", [])
        for imp in imports:
            self.copy("*", root_package=imp, dst="pylon", ignore_case=True)