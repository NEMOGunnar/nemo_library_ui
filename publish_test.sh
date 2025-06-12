#!/bin/bash
set -e  # Stops the script if any command fails
set -x  # Prints each command before executing it (Debugging)

# Remove old distribution artifacts
rm -rf build dist *.egg-info

# Convert README.md to README.rst
pandoc -f markdown -t rst -o README.rst README.md

# Create the distribution
python -m build

# Configure Twine and upload the package
source config_twine_test.sh
twine upload --repository testpypi dist/* -u "$USER" -p "$PWD" --verbose