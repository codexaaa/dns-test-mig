#!/bin/bash
sudo curl -L https://raw.githubusercontent.com/codexaaa/dns-test-mig/main/dns-test-mig.py -o /usr/bin/dns-test-mig

sudo chmod +x /usr/bin/dns-test-mig

echo "----------------------------------------------"
echo "Installation Complete!"
echo "Just type 'dns-test-mig' to start."
echo "----------------------------------------------"
