#!/usr/bin/env python3
import os
import subprocess
import questionary

# List of DNS providers to test
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
    "Algar Telecom": "201.48.24.11",
    "Vivo (Brazil)": "200.204.0.10",
    "Claro/NET (Brazil)": "201.21.192.101",
    "AdGuard (Block Ads)": "94.140.14.14",
    "Mullvad (Privacy)": "194.242.2.2",
    "Control D": "76.76.2.0",
    "CleanBrowsing (Family)": "185.228.168.168",
    "DNS.WATCH": "84.200.69.80",
    "LibreDNS": "116.202.176.26",
    "Comodo Secure": "8.26.56.26",
    "Level3 (Lumen)": "4.2.2.1",
    "Verisign": "64.6.64.6",
    "Oracle (Dyn)": "216.146.35.35",
    "Freenom": "80.80.80.80",
    "Yandex (Russia)": "77.88.8.8",
    "Tencent (China)": "119.29.29.29",
    "AliDNS (Alibaba)": "223.5.5.5",
    "OpenNIC (Global)": "185.121.177.177",
    "Neustar": "156.154.70.1",
    "Hurricane Electric": "74.82.42.42"
}

def get_ping(ip):
    """Returns the average latency in ms."""
    try:
        # Executes 3 pings and gets the average
        output = subprocess.check_output(
            ["ping", "-c", "3", "-n", ip], 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        # Extracts the average time from the ping command output
        avg_ping = output.split('/')[-3]
        return float(avg_ping)
    except:
        return float('inf')

def apply_dns(ip):
    """Applies the DNS via nmcli (NetworkManager)."""
    try:
        # Gets the name of the active connection (e.g., 'Wired connection 1' or 'wlan0')
        conn = subprocess.check_output(
            "nmcli -t -f NAME connection show --active | head -n 1", 
            shell=True, universal_newlines=True
        ).strip()
        
        print(f"\nApplying {ip} to connection: {conn}...")
        
        # Sets the DNS and restarts the interface to apply changes
        os.system(f"nmcli connection modify '{conn}' ipv4.dns '{ip}'")
        os.system(f"nmcli connection modify '{conn}' ipv4.ignore-auto-dns yes")
        os.system(f"nmcli connection up '{conn}'")
        
        print("Success! DNS has been changed.")
    except Exception as e:
        print(f"Error applying DNS: {e}")

def main():
    print("Checking DNS server latency...\n")
    results = []

    for name, ip in DNS_PROVIDERS.items():
        latency = get_ping(ip)
        results.append((name, ip, latency))
        print(f"[{name}] {ip} -> {latency}ms")

    # Sorts by the best ping
    results.sort(key=lambda x: x[2])
    best = results[0]

    print(f"\nThe best DNS found was: {best[0]} ({best[1]}) with {best[2]}ms")

    # Interactive menu
    choice = questionary.select(
        "Which DNS would you like to apply?",
        choices=[f"{r[0]} ({r[1]}) - {r[2]}ms" for r in results] + ["Exit"]
    ).ask()

    if choice != "Exit":
        # Extracts the IP from the choice string
        selected_ip = choice.split('(')[1].split(')')[0]
        apply_dns(selected_ip)

if __name__ == "__main__":
    main()
