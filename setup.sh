#!/bin/bash

# This script will create / load virtual environment, and load the dependencies


if [ ! -d "venv" ]; then
  echo "⏳ Creating venv..."
  python3 -m venv venv
  echo "✅ Venv created!"
fi
source venv/bin/activate
echo "✅ Sucessfully activated environment!"

pip install --upgrade pip

echo "⏳ Installing module in editable mode..."
pip install -e .
echo "✅ Module successfully installed!"

echo "⏳ Installing requirements..."
pip install -r requirements.txt
echo "✅ Requirements succesfully installed!"

pre-commit install

echo "✅ Dev environment is ready!"
