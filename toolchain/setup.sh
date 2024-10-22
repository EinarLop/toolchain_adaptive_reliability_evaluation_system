#!/bin/bash

# Step 1: Install OpenJDK (assumes Ubuntu/Debian-based Linux)
echo "Updating package index..."
sudo apt update -y

echo "Installing OpenJDK (default version)..."
sudo apt install -y default-jdk

# Verify the installation
echo "Verifying Java installation..."
java -version

if [ $? -ne 0 ]; then
    echo "Java installation failed or not found."
    exit 1
else
    echo "Java installed successfully."
fi
# Step 2: Install Python and required packages
echo "Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Verify Python installation
python3 --version

if [ $? -ne 0 ]; then
    echo "Python installation failed or not found."
    exit 1
else
    echo "Python installed successfully."
fi
# Step 3: Activate virtual environment
VENV_DIR="./prism-toolchain-venv"

if [ -d "$VENV_DIR" ]; then
    echo "Activating the virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    if [ $? -eq 0 ]; then
        echo "Virtual environment activated."
    else
        echo "Failed to activate the virtual environment."
        exit 1
    fi
else
    echo "Virtual environment directory 'prism-toolchain-venv' not found in the current directory."
    exit 1
fi
# Step 4: Install Python packages (matplotlib, networkx)
echo "Installing matplotlib and networkx..."
pip install matplotlib networkx

# Verify installation of packages
if [ $? -ne 0 ]; then
    echo "Package installation failed."
    exit 1
else
    echo "Packages installed successfully."
fi
