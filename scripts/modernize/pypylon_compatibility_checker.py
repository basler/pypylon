#!/usr/bin/env python3
"""
PyPylon Compatibility Checker

Main script that orchestrates API extraction and comparison for pypylon.
This replaces pidiff with a custom solution specifically designed for pypylon.
Uses uv for environment management to ensure consistent Python versions.

Usage:
    # Quick check against PyPI version (both using Python 3.14)
    python pypylon_compatibility_checker.py --quick-check
    
    # Full comparison with specific pypylon version
    python pypylon_compatibility_checker.py --full-check --pypylon-version 4.0.0
    
    # Compare specific API dumps
    python pypylon_compatibility_checker.py --compare old_api.json new_api.json
"""

import argparse
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import tempfile
import shutil

# Import our custom modules
try:
    from pypylon_api_dumper import create_api_dump, PylonAPIExtractor
    from pypylon_api_differ import compare_api_dumps, PylonAPIDiffer, load_api_dump
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    print("Make sure pypylon_api_dumper.py and pypylon_api_differ.py are in the same directory")
    sys.exit(1)


class PylonCompatibilityChecker:
    """Main compatibility checker orchestrator"""
    
    def __init__(self, work_dir: str = None):
        self.work_dir = Path(work_dir) if work_dir else Path.cwd() / "compatibility_check_work"
        self.work_dir.mkdir(exist_ok=True)
        
        # Paths for temporary environments and API dumps
        self.reference_env_dir = self.work_dir / "reference_env"
        self.current_env_dir = self.work_dir / "current_env" 
        self.dumps_dir = self.work_dir / "api_dumps"
        self.reports_dir = self.work_dir / "reports"
        
        # Create directories
        for dir_path in [self.dumps_dir, self.reports_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def setup_uv_environment(self, env_name: str, python_version: str = "3.14", 
                           pypylon_version: str = "latest") -> Path:
        """Set up environment using uv with specific Python version"""
        
        print(f"🔧 Setting up {env_name} environment with uv...")
        print(f"   Python: {python_version}")
        print(f"   PyPylon: {pypylon_version}")
        
        env_dir = self.work_dir / env_name
        
        # Clean up existing environment
        if env_dir.exists():
            shutil.rmtree(env_dir)
        
        # Create uv environment with specific Python version
        uv_create_cmd = ["uv", "venv", str(env_dir), "--python", python_version]
        result = subprocess.run(uv_create_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create uv environment: {result.stderr}")
        
        # Get uv environment Python path
        if os.name == 'nt':  # Windows
            venv_python = env_dir / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            venv_python = env_dir / "bin" / "python"
        
        # Install pypylon using uv pip
        if pypylon_version == "local":
            # Install from local source directory (two levels up from scripts/modernize)
            local_source = Path(__file__).parent.parent.parent
            install_cmd = ["uv", "pip", "install", "--python", str(venv_python), str(local_source)]
            print(f"📦 Installing pypylon from local source: {local_source}")
        elif pypylon_version == "latest":
            install_cmd = ["uv", "pip", "install", "--python", str(venv_python), "pypylon"]
            print(f"📦 Installing pypylon {pypylon_version} from PyPI...")
        else:
            install_cmd = ["uv", "pip", "install", "--python", str(venv_python), f"pypylon=={pypylon_version}"]
            print(f"📦 Installing pypylon {pypylon_version} from PyPI...")
        
        result = subprocess.run(install_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Installation failed. Command: {' '.join(install_cmd)}")
            print(f"❌ Error output: {result.stderr}")
            if result.stdout:
                print(f"❌ Standard output: {result.stdout}")
            raise RuntimeError(f"Failed to install pypylon: {result.stderr}")
        
        # Verify installation with robust check
        verify_cmd = [str(venv_python), "-c", """
import pypylon
print(f"PyPylon imported successfully")
try:
    # Try to get version info in different ways
    if hasattr(pypylon, '__version__'):
        print(f"Version: {pypylon.__version__}")
    elif hasattr(pypylon, 'version'):
        print(f"Version: {pypylon.version}")
    elif hasattr(pypylon, 'pylon') and hasattr(pypylon.pylon, 'PylonVersionInfo'):
        print(f"Version: {pypylon.pylon.PylonVersionInfo}")
    else:
        print("Version: available but format unknown")
    
    # Test basic functionality
    submodules = []
    for mod in ['pylon', 'genicam', 'pylondataprocessing']:
        try:
            __import__(f'pypylon.{mod}')
            submodules.append(mod)
        except ImportError:
            pass
    print(f"Available submodules: {', '.join(submodules) if submodules else 'none'}")
except Exception as e:
    print(f"Additional info unavailable: {e}")
"""]
        result = subprocess.run(verify_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to verify pypylon installation: {result.stderr}")
        
        print(f"✅ {env_name} environment ready:")
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        return venv_python
    
    def setup_reference_environment(self, python_version: str = "3.14", 
                                   pypylon_version: str = "latest") -> Path:
        """Set up reference environment with specific pypylon version from PyPI"""
        return self.setup_uv_environment("reference_env", python_version, pypylon_version)
    
    def setup_current_environment(self, python_version: str = "3.14") -> Path:
        """Set up current environment with local pypylon"""
        return self.setup_uv_environment("current_env", python_version, "local")
    
    def get_current_python(self, python_path: str = None) -> Path:
        """Get current Python executable path"""
        if python_path:
            return Path(python_path)
        else:
            return Path(sys.executable)
    
    def create_reference_dump(self, python_exe: Path = None, 
                             pypylon_version: str = "latest") -> Path:
        """Create API dump from reference environment"""
        
        if python_exe is None:
            python_exe = self.setup_reference_environment(pypylon_version=pypylon_version)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = self.dumps_dir / f"pypylon_reference_{pypylon_version}_{timestamp}.json"
        
        print(f"📸 Creating reference API dump...")
        create_api_dump(
            python_executable=str(python_exe),
            output_file=str(dump_file)
        )
        
        return dump_file
    
    def create_current_dump(self, python_exe: Path = None) -> Path:
        """Create API dump from current environment"""
        
        if python_exe is None:
            python_exe = self.setup_current_environment()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = self.dumps_dir / f"pypylon_current_{timestamp}.json"
        
        print(f"📸 Creating current API dump...")
        create_api_dump(
            python_executable=str(python_exe),
            output_file=str(dump_file)
        )
        
        return dump_file
    
    def run_compatibility_check(self, reference_python: str = None,
                               current_python: str = None,
                               pypylon_version: str = "latest",
                               output_format: str = "html") -> None:
        """Run full compatibility check with both environments using uv"""
        
        print("🚀 Starting PyPylon compatibility check...")
        print("=" * 60)
        
        try:
            # Create reference environment and dump
            reference_dump = self.create_reference_dump(pypylon_version=pypylon_version)
            
            # Create current environment and dump
            current_dump = self.create_current_dump()
            
            # Compare dumps
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.reports_dir / f"compatibility_report_{timestamp}.{output_format}"
            
            print(f"🔍 Comparing API dumps...")
            compare_api_dumps(
                reference_file=str(reference_dump),
                current_file=str(current_dump),
                output_file=str(output_file),
                text_only=(output_format == "text")
            )
            
            print(f"✅ Compatibility check completed!")
            print(f"📊 Report saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Compatibility check failed: {e}")
            raise
    
    def quick_check(self, output_format: str = "text") -> None:
        """Quick compatibility check using uv environments"""
        
        print("🚀 Starting quick PyPylon compatibility check...")
        print("=" * 60)
        
        try:
            # Create reference environment and dump
            reference_dump = self.create_reference_dump()
            
            # Create current environment and dump
            current_dump = self.create_current_dump()
            
            # Compare dumps
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.reports_dir / f"compatibility_report_{timestamp}.{output_format}"
            
            print(f"🔍 Comparing API dumps...")
            compare_api_dumps(
                reference_file=str(reference_dump),
                current_file=str(current_dump),
                output_file=str(output_file),
                text_only=(output_format == "text")
            )
            
            print(f"✅ Quick check completed!")
            print(f"📊 Report saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Quick check failed: {e}")
            raise
    
    def compare_existing_dumps(self, reference_file: str, current_file: str,
                              output_file: str = None, output_format: str = "html") -> None:
        """Compare two existing API dump files"""
        
        print(f"📊 Comparing existing API dumps...")
        print(f"   Reference: {reference_file}")
        print(f"   Current: {current_file}")
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_format == "html":
                output_file = str(self.reports_dir / f"comparison_{timestamp}.html")
            else:
                output_file = str(self.reports_dir / f"comparison_{timestamp}.txt")
        
        compare_api_dumps(
            reference_file=reference_file,
            current_file=current_file,
            output_file=output_file,
            text_only=(output_format == "text")
        )
        
        print(f"✅ Comparison completed: {output_file}")
    
    def cleanup(self, keep_dumps: bool = True, keep_reports: bool = True) -> None:
        """Clean up temporary files and environments"""
        
        print("🧹 Cleaning up...")
        
        # Remove temporary environments
        for env_dir in [self.reference_env_dir, self.current_env_dir]:
            if env_dir.exists():
                shutil.rmtree(env_dir)
                print(f"   Removed: {env_dir}")
        
        # Optionally remove dumps and reports
        if not keep_dumps and self.dumps_dir.exists():
            shutil.rmtree(self.dumps_dir)
            print(f"   Removed: {self.dumps_dir}")
        
        if not keep_reports and self.reports_dir.exists():
            shutil.rmtree(self.reports_dir)
            print(f"   Removed: {self.reports_dir}")
    
    def list_dumps(self) -> None:
        """List available API dumps"""
        
        if not self.dumps_dir.exists():
            print("No API dumps found")
            return
        
        dumps = list(self.dumps_dir.glob("*.json"))
        if not dumps:
            print("No API dumps found")
            return
        
        print(f"📁 Available API dumps in {self.dumps_dir}:")
        for dump in sorted(dumps):
            stat = dump.stat()
            size_mb = stat.st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(stat.st_mtime)
            print(f"   {dump.name} ({size_mb:.1f}MB, {mtime.strftime('%Y-%m-%d %H:%M')})")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PyPylon API Compatibility Checker (using uv for environment management)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick compatibility check against latest PyPI version (both using Python 3.14)
  python pypylon_compatibility_checker.py --quick-check
  
  # Full check with specific pypylon version
  python pypylon_compatibility_checker.py --full-check --pypylon-version 4.0.0
  
  # Compare existing API dumps
  python pypylon_compatibility_checker.py --compare old_api.json new_api.json
  
  # Create API dump only
  python pypylon_compatibility_checker.py --dump-only --output my_api.json
  
  # List available dumps
  python pypylon_compatibility_checker.py --list-dumps
        """
    )
    
    # Action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--quick-check", action="store_true",
        help="Run quick compatibility check against latest PyPI version (both using Python 3.14)"
    )
    action_group.add_argument(
        "--full-check", action="store_true",
        help="Run full compatibility check with detailed analysis"
    )
    action_group.add_argument(
        "--compare", nargs=2, metavar=("REFERENCE", "CURRENT"),
        help="Compare two existing API dump files"
    )
    action_group.add_argument(
        "--dump-only", action="store_true",
        help="Create API dump only (no comparison)"
    )
    action_group.add_argument(
        "--list-dumps", action="store_true",
        help="List available API dumps"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--python-version", default="3.14",
        help="Python version to use for both environments (default: 3.14)"
    )
    parser.add_argument(
        "--pypylon-version", default="latest",
        help="PyPylon version to use as reference (default: latest)"
    )
    parser.add_argument(
        "--work-dir",
        help="Working directory for temporary files (default: ./compatibility_check_work)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    parser.add_argument(
        "--format", choices=["html", "text"], default="html",
        help="Output format (default: html)"
    )
    parser.add_argument(
        "--cleanup", action="store_true",
        help="Clean up temporary files after completion"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        checker = PylonCompatibilityChecker(work_dir=args.work_dir)
        
        if args.list_dumps:
            checker.list_dumps()
            
        elif args.dump_only:
            if args.output:
                # Set up current environment and create dump
                checker.setup_current_environment = lambda **kwargs: checker.setup_uv_environment("current_env", args.python_version, "local")
                dump_file = checker.create_current_dump()
                # Copy to specified output location
                import shutil
                shutil.copy2(dump_file, args.output)
                print(f"📄 API dump created: {args.output}")
            else:
                # Set up current environment and create dump
                checker.setup_current_environment = lambda **kwargs: checker.setup_uv_environment("current_env", args.python_version, "local")
                dump_file = checker.create_current_dump()
                print(f"📄 API dump created: {dump_file}")
        
        elif args.compare:
            checker.compare_existing_dumps(
                reference_file=args.compare[0],
                current_file=args.compare[1],
                output_file=args.output,
                output_format=args.format
            )
        
        elif args.quick_check:
            # Update environment setup methods to use the specified Python version
            checker.setup_reference_environment = lambda **kwargs: checker.setup_uv_environment("reference_env", args.python_version, kwargs.get('pypylon_version', 'latest'))
            checker.setup_current_environment = lambda **kwargs: checker.setup_uv_environment("current_env", args.python_version, "local")
            checker.quick_check(output_format=args.format)
        
        elif args.full_check:
            # Update environment setup methods to use the specified Python version
            checker.setup_reference_environment = lambda **kwargs: checker.setup_uv_environment("reference_env", args.python_version, kwargs.get('pypylon_version', args.pypylon_version))
            checker.setup_current_environment = lambda **kwargs: checker.setup_uv_environment("current_env", args.python_version, "local")
            checker.run_compatibility_check(
                pypylon_version=args.pypylon_version,
                output_format=args.format
            )
        
        # Cleanup if requested
        if args.cleanup:
            checker.cleanup()
        
        print(f"\n✅ Operation completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 