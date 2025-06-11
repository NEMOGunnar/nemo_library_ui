# Ensure the script stops on errors
$ErrorActionPreference = "Stop"

# Pull the latest changes from the Git repository
git pull

# Update Conda
conda update -n base -c defaults conda -y

# Activate the Conda environment
conda activate nemo_library_ui

# Display the Python version
python --version

# Upgrade pip
python -m pip install --upgrade pip

# Install or upgrade the required Python packages
pip install --upgrade -r requirements.txt