#!/usr/bin/env python
"""Test coverage runner for pypylon."""

import os
import runpy
import shutil
import sys
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


def run_script_file(script_path):
    """Run a Python file as __main__ while preserving process state."""
    script_dir = str(script_path.parent.resolve())
    script_file = str(script_path.resolve())
    old_argv = sys.argv[:]
    had_dir = script_dir in sys.path

    if not had_dir:
        sys.path.insert(0, script_dir)

    sys.argv = [script_file]
    try:
        runpy.run_path(script_file, run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0, False):
            print(f"Script failed (exit={exc.code}): {script_path}")
    finally:
        sys.argv = old_argv
        if not had_dir:
            sys.path.remove(script_dir)


def run_coverage_on_files(file_pattern):
    """
    Run coverage on files matching the pattern.
    
    Args:
        file_pattern: Glob pattern for test files
        file_pattern: Glob pattern for Python files
    """
    base_path = Path('.')
    files = sorted(base_path.glob(file_pattern))
    
    if not files:
        print(f"No files matching pattern: {file_pattern}")
        return
    
    for test_file in files:
        print(f"Running coverage on: {test_file}")
        run_script_file(test_file)


def main():
    """Run the full coverage suite."""
    original_dir = os.getcwd()
    
    try:
        # Change to tests directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("=== Cleaning up old coverage data ===")
        cleanup_coverage_artifacts()

        cov = coverage.Coverage(source=['pypylon'], branch=True, data_file='.coverage')
        cov.start()
        try:
            print("\n=== Running coverage on genicam tests ===")
            run_coverage_on_files('genicam/*test.py')

            print("\n=== Running coverage on pylon/emulated tests ===")
            os.chdir('pylon/emulated')
            run_coverage_on_files('*test.py')
            os.chdir('../..')

            print("\n=== Running coverage on pylon/gigE tests ===")
            os.chdir('pylon/gigE')
            run_coverage_on_files('*test.py')
            os.chdir('../..')

            print("\n=== Running coverage on pylon/usb tests ===")
            os.chdir('pylon/usb')
            run_coverage_on_files('*test.py')
            os.chdir('../..')

            print("\n=== Running coverage on samples ===")
            os.chdir('../samples/pylon')
            run_coverage_on_files('**/*.py')
            os.chdir('../../tests')
        finally:
            cov.stop()
            cov.save()

        print("\n=== Generating HTML report ===")
        cov.html_report(directory='htmlcov')

        print("\nCoverage report generated in: htmlcov/index.html")
        
    finally:
        os.chdir(original_dir)


if __name__ == '__main__':
    main()
