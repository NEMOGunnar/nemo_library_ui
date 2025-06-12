#!/bin/sh
git pull
conda update -n base -c defaults conda
conda activate nemo_library_ui
python --version
python -m pip install --upgrade pip
pip install -e .
