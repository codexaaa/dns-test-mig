#!/bin/bash

# 1. Configuration & System Detection
APP_NAME="dns-test-mig"
INSTALL_PATH="/usr/local/bin/$APP_NAME"
RAW_URL="https://raw.githubusercontent.com/codexaaa/dns-test-mig/main/dns-test-mig.py"

# This line detects the OS name (e.g., Pop!_OS, Ubuntu)
SISTEMA=$(grep -P '^NAME=' /etc/os-release | cut -d'=' -f2 | sed 's/"//g')

echo "----------------------------------------------"
echo "Starting $APP_NAME installation for $SISTEMA"
echo "----------------------------------------------"

# 2. Update and install system dependencies
echo "[1/4] Checking dependencies (Python3, Pip, and Curl)..."
sudo apt update -y && sudo apt install -y python3 python3-pip curl

# 3. Install the required Python library
# Using --break-system-packages for modern Linux environments
echo "[2/4] Installing 'questionary' library..."
pip3 install questionary --break-system-packages --quiet

# 4. Download the Python script
echo "[3/4] Downloading script from GitHub..."
sudo curl -L "$RAW_URL" -o "$INSTALL_PATH"

# 5. Set permissions
echo "[4/4] Setting execution permissions..."
sudo chmod +x "$INSTALL_PATH"

echo "----------------------------------------------"
echo "INSTALLATION COMPLETE!"
echo "System detected: $SISTEMA"
echo "You can now type '$APP_NAME' to start."
echo "----------------------------------------------"
