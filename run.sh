#!/usr/bin/env bash

set -e
set -x

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install CUTEst
git clone --depth 1 --branch v2.0.6 https://github.com/ralna/ARCHDefs "$ARCHDEFS"
git clone --depth 1 --branch v2.0.3 https://github.com/ralna/SIFDecode "$SIFDECODE"
git clone --depth 1 --branch v2.0.3 https://github.com/ralna/CUTEst "$CUTEST"
git clone --depth 1 --branch v0.5 https://bitbucket.org/optrove/sif "$MASTSIF"
export ARCHDEFS
export SIFDECODE
export CUTEST
export MASTSIF
export MYARCH
bash -c "$(curl -fsSL https://raw.githubusercontent.com/jfowkes/pycutest/master/.install_cutest.sh)"

# Install other requirements
python -m pip install --progress-bar=off -r requirements.txt

# Run the performance and data profile comparisons
export PYCUTEST_CACHE=$PWD
python main.py
