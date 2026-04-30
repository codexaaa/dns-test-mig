#!/usr/bin/env python3
import os
import subprocess
import questionary

# List of DNS providers to test
DNS_PROVIDERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS": "208.67.222.222",
    "Quad9": "9.9.9.9",
    "AdGuard": "94.140.14.14",
    "Local (Gateway)": "192.168.1.1"
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
