import os
import subprocess
import questionary

# Lista de DNS para testar
DNS_PROVIDERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS": "208.67.222.222",
    "Quad9": "9.9.9.9",
    "Local (Gateway)": "192.168.1.1"
}

def get_ping(ip):
    """Retorna a latência média em ms."""
    try:
        # Executa 3 pings e pega a média
        output = subprocess.check_output(
            ["ping", "-c", "3", "-n", ip], 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        # Extrai o tempo médio da saída do comando ping
        avg_ping = output.split('/')[-3]
        return float(avg_ping)
    except:
        return float('inf')

def apply_dns(ip):
    """Aplica o DNS via nmcli (NetworkManager)."""
    try:
        # Pega o nome da conexão ativa (ex: 'Wired connection 1' ou 'wlan0')
        conn = subprocess.check_output(
            "nmcli -t -f NAME connection show --active | head -n 1", 
            shell=True, universal_newlines=True
        ).strip()
        
        print(f"\nAplicando {ip} na conexão: {conn}...")
        
        # Define o DNS e reinicia a interface para aplicar
        os.system(f"nmcli connection modify '{conn}' ipv4.dns '{ip}'")
        os.system(f"nmcli connection modify '{conn}' ipv4.ignore-auto-dns yes")
        os.system(f"nmcli connection up '{conn}'")
        
        print("Sucesso! DNS alterado.")
    except Exception as e:
        print(f"Erro ao aplicar: {e}")

def main():
    print("Verificando latência dos servidores DNS...\n")
    results = []

    for name, ip in DNS_PROVIDERS.items():
        latency = get_ping(ip)
        results.append((name, ip, latency))
        print(f"[{name}] {ip} -> {latency}ms")

    # Ordena pelo melhor ping
    results.sort(key=lambda x: x[2])
    best = results[0]

    print(f"\nO melhor DNS encontrado foi: {best[0]} ({best[1]}) com {best[2]}ms")

    # Menu interativo
    choice = questionary.select(
        "Deseja aplicar qual DNS?",
        choices=[f"{r[0]} ({r[1]}) - {r[2]}ms" for r in results] + ["Sair"]
    ).ask()

    if choice != "Sair":
        # Extrai o IP da string de escolha
        selected_ip = choice.split('(')[1].split(')')[0]
        apply_dns(selected_ip)

if __name__ == "__main__":
    main()