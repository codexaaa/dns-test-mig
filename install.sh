#!/bin/bash
echo "Installing DNS Test Mig..."

# Atualiza e instala dependências do sistema
sudo apt update
sudo apt install -y python3 python3-pip network-manager curl

# Instala a biblioteca do menu interativo
pip3 install questionary --break-system-packages --quiet

# Baixa o seu script Python e o move para a pasta de executáveis do sistema
sudo curl -L https://raw.githubusercontent.com/codexaaa/dns-test-mig/main/dns-test-mig.py -o /usr/bin/dns-test-mig

# Torna o arquivo executável
sudo chmod +x /usr/bin/dns-test-mig

echo "----------------------------------------------"
echo "Installation Complete!"
echo "Just type 'dns-test-mig' to start."
echo "----------------------------------------------"
