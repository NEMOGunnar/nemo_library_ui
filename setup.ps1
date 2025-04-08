git pull
conda update -n base -c defaults conda
conda activate nemo_library
python --version
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
# pip freeze > requirements.txt
pip freeze | ForEach-Object { ($_ -split "==")[0] -replace " @.*", "" } > requirements.txt
