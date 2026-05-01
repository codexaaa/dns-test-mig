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
    },
    "es_ES": {
        "checking": "Comprobando la latencia de los servidores DNS...",
        "best_found": "\nEl mejor DNS encontrado fue: {} ({}) con {}ms",
        "menu_title": "¿Qué DNS le gustaría aplicar?",
        "exit": "Salir",
        "no_conn": "¡No se encontró ninguna conexión activa!",
        "applying": "\nAplicando {} a la conexión: '{}'...",
        "success": "¡Éxito! El DNS ha sido cambiado.",
        "error": "Error al aplicar el DNS: {}",
        "parse_error": "No se pudo extraer la dirección IP de la selección."
    },
    "fr_FR": {
        "checking": "Vérification de la latence des serveurs DNS...",
        "best_found": "\nLe meilleur DNS trouvé était : {} ({}) avec {}ms",
        "menu_title": "Quel DNS souhaitez-vous appliquer ?",
        "exit": "Quitter",
        "no_conn": "Aucune connexion active trouvée !",
        "applying": "\nApplication de {} à la connexion : '{}'...",
        "success": "Succès ! Le DNS a été modifié.",
        "error": "Erreur lors de l'application du DNS : {}",
        "parse_error": "Impossible d'extraire l'adresse IP de la sélection."
    },
    "de_DE": {
        "checking": "DNS-Server-Latenz wird geprüft...",
        "best_found": "\nDer beste gefundene DNS war: {} ({}) mit {}ms",
        "menu_title": "Welchen DNS möchten Sie anwenden?",
        "exit": "Beenden",
        "no_conn": "Keine aktive Verbindung gefunden!",
        "applying": "\n{} wird auf Verbindung '{}' angewendet...",
        "success": "Erfolg! DNS wurde geändert.",
        "error": "Fehler beim Anwenden des DNS: {}",
        "parse_error": "IP-Adresse konnte nicht aus der Auswahl extrahiert werden."
    },
    "it_IT": {
        "checking": "Verifica della latenza dei server DNS...",
        "best_found": "\nIl miglior DNS trovato è stato: {} ({}) con {}ms",
        "menu_title": "Quale DNS vorresti applicare?",
        "exit": "Esci",
        "no_conn": "Nessuna connessione attiva trovata!",
        "applying": "\nApplicazione di {} alla connessione: '{}'...",
        "success": "Successo! Il DNS è stato modificato.",
        "error": "Errore durante l'applicazione del DNS: {}",
        "parse_error": "Impossibile estrarre l'indirizzo IP dalla selezione."
    }
}

# Detect language
try:
    current_locale = locale.getdefaultlocale()[0] or "en_US"
except:
    current_locale = "en_US"

texts = LANG_DATA.get(current_locale, LANG_DATA["en_US"])

# --- DNS PROVIDERS ---
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
    """Returns average latency in ms."""
    try:
        # -c 3 is for Linux/macOS. For Windows it would be -n 3
        output = subprocess.check_output(
            ["ping", "-c", "3", "-n", ip], 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        # Extracting avg from "min/avg/max/mdev = 10.123/12.456/..."
        avg_ping = output.split('/')[-3]
        return float(avg_ping)
    except:
        return float('inf')

def apply_dns(ip):
    """Applies DNS via nmcli with sudo."""
    try:
        conn = subprocess.check_output(
            "nmcli -t -f NAME connection show --active | head -n 1", 
            shell=True, universal_newlines=True
        ).strip()
        
        if not conn:
            print(texts["no_conn"])
            return

        print(texts["applying"].format(ip, conn))
        
        # Using subprocess.run for better command handling
        subprocess.run(["sudo", "nmcli", "connection", "modify", conn, "ipv4.dns", ip], check=True)
        subprocess.run(["sudo", "nmcli", "connection", "modify", conn, "ipv4.ignore-auto-dns", "yes"], check=True)
        subprocess.run(["sudo", "nmcli", "connection", "up", conn], check=True)
        
        print(texts["success"])
    except Exception as e:
        print(texts["error"].format(e))

def main():
    print(texts["checking"] + "\n")
    results = []

    for name, ip in DNS_PROVIDERS.items():
        latency = get_ping(ip)
        results.append((name, ip, latency))
        # Optional: Print progress
        status = f"{latency}ms" if latency != float('inf') else "TIMEOUT"
        print(f"[{name}] {ip} -> {status}")

    results.sort(key=lambda x: x[2])
    best = results[0]

    if best[2] == float('inf'):
        print("\nNo servers responded.")
        return

    print(texts["best_found"].format(best[0], best[1], best[2]))
    
    choices = [f"{r[0]} | {r[1]} | {r[2]}ms" for r in results if r[2] != float('inf')]
    choices.append(texts["exit"])

    choice = questionary.select(
        texts["menu_title"],
        choices=choices
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
