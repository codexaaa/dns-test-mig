#!/bin/bash

if [ -d "$PREFIX/bin" ]; then
    # Configuração para Termux
    DESTINO="$PREFIX/bin/dns-test-mig"
    CMD_INSTALL="pip install questionary"
    SUDO=""
else
    DESTINO="/usr/local/bin/dns-test-mig"
    CMD_INSTALL="pip3 install questionary --break-system-packages"
    SUDO="sudo"
fi

echo "Installing dependencies..."
$CMD_INSTALL

echo "Downloading DNS Test by Mig..."
$SUDO curl -L https://raw.githubusercontent.com/codexaaa/dns-test-mig/main/dns-test-mig.py -o $DESTINO

echo "Setting permissions..."
$SUDO chmod +x $DESTINO

echo "----------------------------------------------"
echo "Installation Complete!"
echo "Just type 'dns-test-mig' to start."
echo "----------------------------------------------"
