#!/bin/bash

echo "Starting uninstallation of DNS Test Mig..."

if [ -d "$PREFIX/bin" ]; then
    rm -f "$PREFIX/bin/dns-test-mig"
    echo "Removed from Termux bin."
fi

if [ -f "/usr/local/bin/dns-test-mig" ]; then
    sudo rm "/usr/local/bin/dns-test-mig"
    echo "Removed from /usr/local/bin."
fi

if [ -f "/usr/bin/dns-test-mig" ]; then
    sudo rm "/usr/bin/dns-test-mig"
    echo "Removed from /usr/bin."
fi

echo "----------------------------------------------"
echo "Uninstallation Complete :("
echo "----------------------------------------------"
