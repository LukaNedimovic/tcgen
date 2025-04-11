#!/bin/bash

# This script will create / load virtual environment, and load the dependencies

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

pip install --upgrade pip
pip install -e .
pip install -r requirements.txt

pre-commit install

echo "✅ Dev environment is ready!"
