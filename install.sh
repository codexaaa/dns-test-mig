#!/bin/bash
# Baixa o código do seu GitHub
sudo curl -L https://raw.githubusercontent.com/codexaaa/dns-test-mig/main/dns-test-mig.py -o /usr/bin/dns-test-mig

# DÁ A PERMISSÃO DE EXECUÇÃO (Isso é o que está faltando!)
sudo chmod +x /usr/bin/dns-test-mig

echo "----------------------------------------------"
echo "Installation Complete!"
echo "Just type 'dns-test-mig' to start."
echo "----------------------------------------------"
