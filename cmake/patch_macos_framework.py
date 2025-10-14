#!/usr/bin/env python3
"""
Patch macOS pylon.framework for macOS 14+ compatibility.

This script patches the pylon-libusb library to set the correct minimum
macOS version and SDK version, then re-signs the framework with an ad-hoc signature.
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path


def patch_libusb_for_macos14(framework_path):
    """
    Patch pylon-libusb to work with macOS 14+.
    
    Args:
        framework_path: Path to pylon.framework directory
    """
    try:
        import lief
    except ImportError:
        print("Warning: LIEF not available, skipping libusb patching")
        print("Install LIEF with: pip install lief")
        return False
    
    framework_path = Path(framework_path)
    if not framework_path.exists():
        print(f"Error: Framework path does not exist: {framework_path}")
        return False
    
    print(f"Searching for pylon-libusb libraries in {framework_path}...")
    
    # Find all pylon-libusb files
    libusb_files = list(framework_path.glob("**/pylon-libusb-*.dylib"))
    
    if not libusb_files:
        print("No pylon-libusb libraries found, skipping patching")
        return True
    
    for libusb_file in libusb_files:
        print(f"\nPatching {libusb_file.name} for macOS 14+ compatibility...")
        
        try:
            # Parse the Mach-O file (might be a fat/universal binary)
            fat_binary = lief.MachO.parse(str(libusb_file))
            
            if not fat_binary:
                print(f"  Warning: Could not parse {libusb_file.name}")
                continue
            
            # Patch each architecture in the binary
            patched = False
            for binary in fat_binary:
                arch_name = f"{binary.header.cpu_type}"
                print(f"  Patching architecture: {arch_name}")
                
                for command in binary.commands:
                    if isinstance(command, lief.MachO.BuildVersion):
                        old_minos = command.minos
                        old_sdk = command.sdk
                        command.minos = (14, 0, 0)  # Set macOS 14.0 as minimum version
                        command.sdk = (14, 0, 0)    # Set macOS SDK 14.0
                        print(f"    Changed minos from {old_minos} to {command.minos}")
                        print(f"    Changed SDK from {old_sdk} to {command.sdk}")
                        patched = True
            
            if patched:
                # Write the patched binary back
                print(f"  Writing patched binary...")
                fat_binary.write(str(libusb_file))
                
                # Re-sign with ad-hoc signature
                print(f"  Creating ad-hoc signature for {libusb_file.name}...")
                result = subprocess.run(
                    ["codesign", "--force", "-s", "-", str(libusb_file)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"  Warning: codesign failed: {result.stderr}")
                else:
                    print(f"  Successfully signed {libusb_file.name}")
            else:
                print(f"  No BuildVersion commands found to patch")
                
        except Exception as e:
            print(f"  Error patching {libusb_file.name}: {e}")
            return False
    
    # Re-sign the entire framework
    print(f"\nSigning framework: {framework_path.name}")
    result = subprocess.run(
        ["codesign", "--force", "--deep", "-s", "-", str(framework_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Warning: Framework signing failed: {result.stderr}")
    else:
        print(f"Successfully signed {framework_path.name}")
    
    return True


def patch_wheel(wheel_path):
    """
    Patch a wheel file by extracting, patching frameworks, and repacking.
    
    Args:
        wheel_path: Path to the wheel file
    """
    from zipfile import ZipFile
    import tempfile
    import shutil
    
    wheel_path = Path(wheel_path)
    if not wheel_path.exists():
        print(f"Error: Wheel file does not exist: {wheel_path}")
        return False
    
    print(f"\nPatching wheel: {wheel_path.name}")
    
    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_path = temp_path / "wheel_contents"
        
        print("Extracting wheel...")
        with ZipFile(wheel_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # Find and patch pylon.framework
        framework_dirs = list(extract_path.glob("**/pylon.framework"))
        
        if not framework_dirs:
            print("No pylon.framework found in wheel, skipping patching")
            return True
        
        success = True
        for framework_dir in framework_dirs:
            print(f"\nFound framework at: {framework_dir.relative_to(extract_path)}")
            if not patch_libusb_for_macos14(framework_dir):
                success = False
        
        if not success:
            return False
        
        # Repack the wheel
        print("\nRepacking wheel...")
        backup_path = wheel_path.with_suffix('.bak')
        wheel_path.rename(backup_path)
        
        try:
            with ZipFile(wheel_path, 'w') as zip_out:
                for file_path in extract_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(extract_path)
                        zip_out.write(file_path, arcname)
            
            # Remove backup if successful
            backup_path.unlink()
            print(f"Successfully patched and repacked wheel: {wheel_path.name}")
            return True
            
        except Exception as e:
            # Restore backup on error
            print(f"Error repacking wheel: {e}")
            wheel_path.unlink(missing_ok=True)
            backup_path.rename(wheel_path)
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: patch_macos_framework.py <framework_or_wheel_path>")
        print("\nPatches pylon.framework for macOS 14+ compatibility.")
        print("Can accept either a path to pylon.framework or a wheel file.")
        sys.exit(1)
    
    target_path = Path(sys.argv[1])
    
    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(1)
    
    # Determine if this is a wheel or a framework directory
    if target_path.suffix == '.whl':
        success = patch_wheel(target_path)
    elif target_path.name.endswith('.framework') or (target_path / 'pylon.framework').exists():
        # Handle both direct framework path and parent directory
        if target_path.name.endswith('.framework'):
            success = patch_libusb_for_macos14(target_path)
        else:
            framework = target_path / 'pylon.framework'
            success = patch_libusb_for_macos14(framework)
    else:
        print(f"Error: Unknown target type: {target_path}")
        print("Expected either a .whl file or a .framework directory")
        sys.exit(1)
    
    if not success:
        print("\n❌ Patching failed")
        sys.exit(1)
    
    print("\n✅ Patching completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()

