#!/usr/bin/env python
"""Test coverage runner for pypylon."""

import os
import shutil
import sys
import unittest
from pathlib import Path

try:
    import coverage
except ImportError:
    print("Error: coverage module not installed. Install with: pip install coverage")
    sys.exit(1)


def cleanup_coverage_artifacts():
    """Remove old coverage files and reports."""
    paths_to_remove = [
        'htmlcov',
        '.coverage',
        'pylon/gigE/.coverage',
        'pylon/emulated/.coverage',
        'pylon/usb/.coverage',
        '../samples/.coverage',
    ]
    
    for path in paths_to_remove:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                print(f"Removed file: {path}")
        except FileNotFoundError:
            pass


def run_coverage_on_files(file_pattern, use_unittest=False):
    """
    Run coverage on files matching the pattern.
    
    Args:
        file_pattern: Glob pattern for test files
        use_unittest: If True, run as unittest modules
    """
    base_path = Path('.')
    files = sorted(base_path.glob(file_pattern))
    
    if not files:
        print(f"No files matching pattern: {file_pattern}")
        return
    
    for test_file in files:
        print(f"Running coverage on: {test_file}")
        
        cov = coverage.Coverage(source=['pypylon'], branch=True, data_file='.coverage')
        cov.start()
        
        try:
            if use_unittest:
                module_name = str(test_file).replace('.py', '').replace('/', '.')
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromName(module_name)
                runner = unittest.TextTestRunner(verbosity=0)
                runner.run(suite)
            else:
                module_name = str(test_file).replace('.py', '').replace('/', '.')
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromName(module_name)
                runner = unittest.TextTestRunner(verbosity=0)
                runner.run(suite)
        finally:
            cov.stop()
            cov.save()


def main():
    """Run the full coverage suite."""
    original_dir = os.getcwd()
    
    try:
        # Change to tests directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("=== Cleaning up old coverage data ===")
        cleanup_coverage_artifacts()
        
        print("\n=== Running coverage on genicam tests ===")
        run_coverage_on_files('genicam/*test.py', use_unittest=False)
        
        print("\n=== Running coverage on pylon/emulated tests ===")
        os.chdir('pylon/emulated')
        run_coverage_on_files('*test.py', use_unittest=True)
        os.chdir('../..')
        
        print("\n=== Running coverage on pylon/gigE tests ===")
        os.chdir('pylon/gigE')
        run_coverage_on_files('*test.py', use_unittest=True)
        os.chdir('../..')
        
        print("\n=== Running coverage on pylon/usb tests ===")
        os.chdir('pylon/usb')
        run_coverage_on_files('*test.py', use_unittest=True)
        os.chdir('../..')
        
        print("\n=== Running coverage on samples ===")
        os.chdir('../samples/pylon')
        run_coverage_on_files('**/*.py', use_unittest=False)
        os.chdir('../../tests')
        
        print("\n=== Combining coverage data ===")
        cov = coverage.Coverage(data_file='.coverage')
        cov.combine()
        
        print("\n=== Generating HTML report ===")
        cov.load()
        cov.html_report(directory='htmlcov')
        
        print("\nCoverage report generated in: htmlcov/index.html")
        
    finally:
        os.chdir(original_dir)


if __name__ == '__main__':
    main()
