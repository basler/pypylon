#!/bin/zsh

# Remove coverage artifacts
rm -rf htmlcov
rm -f .coverage
rm -f pylon/gigE/.coverage
rm -f pylon/emulated/.coverage
rm -f pylon/usb/.coverage
rm -f ../samples/.coverage

# Run coverage on genicam tests
for f in genicam/*test.py; do
    coverage run -a -L --source=pypylon --branch "$f"
done

# Run coverage on emulated tests
pushd pylon/emulated
for f in *test.py; do
    coverage run -a -L --source=pypylon --branch -m unittest "$f"
done
popd

# Run coverage on gigE tests
pushd pylon/gigE
for f in *test.py; do
    coverage run -a -L --source=pypylon --branch -m unittest "$f"
done
popd

# Run coverage on usb tests
pushd pylon/usb
for f in *test.py; do
    coverage run -a -L --source=pypylon --branch -m unittest "$f"
done
popd

# Run coverage on samples
pushd ../samples/pylon
for f in **/*.py; do
    coverage run -a -L --source=pypylon --branch "$f"
done
popd

# Combine coverage data (back in tests directory)
cd ../tests
coverage combine -a .coverage pylon/gigE/.coverage
coverage combine -a .coverage pylon/usb/.coverage
coverage combine -a .coverage pylon/emulated/.coverage
coverage combine -a .coverage ../samples/.coverage

# Generate HTML report
coverage html
