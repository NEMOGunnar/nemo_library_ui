#!/bin/bash
set -e  # Stops the script if any command fails
set -x  # Prints each command before executing it (Debugging)

# Remove old distribution artifacts
rm -rf build dist *.egg-info

# Create the distribution
python -m build

# Configure Twine and upload the package
source config_twine_prod.sh
twine upload dist/* -u "$USER" -p "$PWD" --verbose