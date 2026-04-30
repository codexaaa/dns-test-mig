#!/usr/bin/env python3
import os
import subprocess
import questionary
import re
import locale

LANG_DATA = {
    "pt_BR": {
        "checking": "Verificando a latência dos servidores DNS...",
        "best_found": "\nO melhor DNS encontrado foi: {} ({}) com {}ms",
        "menu_title": "Qual DNS você gostaria de aplicar?",
        "exit": "Sair",
        "no_conn": "Nenhuma conexão ativa encontrada!",
        "applying": "\nAplicando {} à conexão: '{}'...",
        "success": "Sucesso! O DNS foi alterado.",
        "error": "Erro ao aplicar DNS: {}",
        "parse_error": "Não foi possível extrair o endereço IP da seleção."
    },
    "en_US": {
        "checking": "Checking DNS server latency...",
        "best_found": "\nThe best DNS found was: {} ({}) with {}ms",
        "menu_title": "Which DNS would you like to apply?",
        "exit": "Exit",
        "no_conn": "No active connection found!",
        "applying": "\nApplying {} to connection: '{}'...",
        "success": "Success! DNS has been changed.",
        "error": "Error applying DNS: {}",
        "parse_error": "Could not parse IP address from selection."
    }
}

try:
    current_locale = locale.getdefaultlocale()[0]
except:
    current_locale = "en_US"

texts = LANG_DATA.get(current_locale, LANG_DATA["en_US"])

# --- LISTA DE PROVEDORES DNS ---
DNS_PROVIDERS = {
    "Google 1": "8.8.8.8",
    "Google 2": "8.8.4.4",
    "Cloudflare 1": "1.1.1.1",
    "Cloudflare 2": "1.0.0.1",
    "OpenDNS (Cisco)": "208.67.222.222",
    "Quad9 (Secure)": "9.9.9.9",
    "GigaDNS 1": "189.38.95.95",
    "GigaDNS 2": "189.38.95.96",
    "Umbler (Brazil)": "187.84.150.123",
    "AdGuard (Block Ads)": "94.140.14.14",
    "Mullvad (Privacy)": "194.242.2.2",
    "Control D": "76.76.2.0",
    "CleanBrowsing (Family)": "185.228.168.168",
    "DNS.WATCH": "84.200.69.80",
    "LibreDNS": "116.202.176.26",
    "Comodo Secure": "8.26.56.26",
    "Level3 (Lumen)": "4.2.2.1",
    "Verisign": "64.6.64.6",
    "Freenom": "80.80.80.80",
    "Yandex (Russia)": "77.88.8.8",
    "Tencent (China)": "119.29.29.29",
    "AliDNS (Alibaba)": "223.5.5.5",
    "Neustar": "156.154.70.1",
    "Hurricane Electric": "74.82.42.42"
}

def get_ping(ip):
    """Retorna a latência média em ms."""
    try:
        output = subprocess.check_output(
            ["ping", "-c", "3", "-n", ip], 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        avg_ping = output.split('/')[-3]
        return float(avg_ping)
    except:
        return float('inf')

def apply_dns(ip):
    """Aplica o DNS via nmcli com sudo."""
    try:
        conn = subprocess.check_output(
            "nmcli -t -f NAME connection show --active | head -n 1", 
            shell=True, universal_newlines=True
        ).strip()
        
        if not conn:
            print(texts["no_conn"])
            return

        print(texts["applying"].format(ip, conn))
        
        os.system(f"sudo nmcli connection modify '{conn}' ipv4.dns '{ip}'")
        os.system(f"sudo nmcli connection modify '{conn}' ipv4.ignore-auto-dns yes")
        os.system(f"sudo nmcli connection up '{conn}'")
        
        print(texts["success"])
    except Exception as e:
        print(texts["error"].format(e))

def main():
    print(texts["checking"] + "\n")
    results = []

    for name, ip in DNS_PROVIDERS.items():
        latency = get_ping(ip)
        results.append((name, ip, latency))
        print(f"[{name}] {ip} -> {latency}ms")

    results.sort(key=lambda x: x[2])
    best = results[0]

    print(texts["best_found"].format(best[0], best[1], best[2]))
    
    choice = questionary.select(
        texts["menu_title"],
        choices=[f"{r[0]} | {r[1]} | {r[2]}ms" for r in results] + [texts["exit"]]
    ).ask()

    if choice and choice != texts["exit"]:
        
        ip_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        match = re.search(ip_pattern, choice)
        if match:
            selected_ip = match.group(1)
            apply_dns(selected_ip)
        else:
            print(texts["parse_error"])

if __name__ == "__main__":
    main()
