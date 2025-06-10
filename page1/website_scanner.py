#!/usr/bin/env python3
# coding: utf-8

import socket, ssl, requests, ipaddress, json, time, shutil, sys, urllib3, warnings, os

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# ─── Couleurs ANSI 256 ────────────────────────────────────────────────────────
PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
RED           = '\033[38;5;196m'
RESET         = '\033[0m'
BOLD          = '\033[1m'

# ─── ASCII art en un seul bloc (animation conservée) ─────────────────────────
ASCII_ART = r"""

                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                               >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
             >@@| 
                              
"""

# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─── Fonctions utilitaires ────────────────────────────────────────────────────
def print_ascii_art():
    """Affiche l’ASCII art en conservant l’animation ligne par ligne."""
    term_w = shutil.get_terminal_size((80, 20)).columns
    for ln in ASCII_ART.strip('\n').splitlines():
        pad = max((term_w - len(ln)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + ln + RESET)
        time.sleep(0.025)

def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def resolve_domain(domain: str) -> str | None:
    """Renvoie l’adresse IPv4 du domaine ou None si échec."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def fetch_ip_info(ip: str) -> dict | None:
    """Interroge ipinfo.io pour avoir l’ISP / ORG / AS…"""
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        return r.json() if r.status_code == 200 else None
    except requests.RequestException:
        return None

# Ports fréquents + étiquette
COMMON_PORTS = {
    21:  "FTP",
    22:  "SSH",
    25:  "SMTP",
    53:  "DNS",
    80:  "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306:"MySQL",
    8080:"HTTP‑Alt",
    8443:"HTTPS‑Alt",
}

def scan_ports(ip: str, timeout: float = 0.5) -> list[str]:
    """Renvoie une liste "port/PROTO" ouverts parmi COMMON_PORTS."""
    open_ports = []
    for port, proto in COMMON_PORTS.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(f"{port}/{proto}")
    return open_ports

def http_status(url: str) -> int | None:
    """Retourne le code‑statut HTTP (GET) ou None si unreachable."""
    try:
        r = requests.get(url, timeout=6, allow_redirects=True, verify=False)
        return r.status_code
    except requests.RequestException:
        return None

# ─── Affichage des résultats ─────────────────────────────────────────────────
def show_result(data: dict):
    """Affiche les données formatées avec la déco [+]."""
    label_w = max(len(key) for key in data) + 2
    for k, v in data.items():
        val = v if v else "Non disponible"
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} {k.ljust(label_w)}: {WHITE}{val}{RESET}")

# ─── Point d’entrée ──────────────────────────────────────────────────────────
def run():
    clear_screen()
    os.system("title iS-Tools - Website Scanner") 
    print_ascii_art()
    print(f"{PURPLE_LIGHT}===== Website Scanner - tapez 'q' pour quitter ====={RESET}")
    while True:
        target = input(f"{PURPLE_LIGHT}[Website Scanner] - {WHITE}Entrez un domaine : {RESET}").strip()
        if target.lower() in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break

        # ── Nettoyage entrée
        domain = target.replace("http://", "").replace("https://", "").split('/')[0]

        # 👉 message « Scan en cours… »
        print(f"{PURPLE_LIGHT}[Website Scanner] - {WHITE}Scan de {domain}...{RESET}")

        url = "https://" + domain          # on force HTTPS pour commencer
        secure = True

        # ── Test HTTPS – si KO on retente HTTP
        status = http_status(url)
        if status is None:
            url = "http://" + domain
            secure = False
            status = http_status(url)

        # ── Résolution DNS
        ip = resolve_domain(domain)
        ip_status = "VALID" if ip and is_valid_ip(ip) else "INVALID"

        # ── Infos IP
        isp = org = asn = ""
        if ip:
            info = fetch_ip_info(ip)
            if info:
                org_field = info.get("org", "")
                org_parts = org_field.split()
                if org_parts and org_parts[0].startswith("AS"):
                    asn = " ".join(org_parts[:2])
                    isp = " ".join(org_parts[2:])
                    org = isp
                hostname = info.get("hostname") or ""

        # ── Scan ports
        ports_open = ", ".join(scan_ports(ip)) if ip else ""

        # ── Présentation
        result = {
            "Website"     : url,
            "Domain"      : domain,
            "Secure"      : str(secure),
            "Status Code" : status if status is not None else "Indisponible",
            "IP"          : ip or "Non résolu",
            "IP Status"   : ip_status,
            "Host ISP"    : isp,
            "Host ORG"    : org,
            "Host AS"     : asn,
            "Open Port"   : ports_open,
        }
        print()
        print(f"{PURPLE_LIGHT}{BOLD}┌────────────────── [Website Scanner] ──────────────────┐{RESET}")
        show_result(result)
        print(f"{PURPLE_LIGHT}{BOLD}└───────────────────────────────────────────────────────┘{RESET}")
        print()

if __name__ == "__main__":
    # Désactive l’avertissement SSL (self‑signed, etc.) quand verify=False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterruption par l’utilisateur.")
        sys.exit(0)
