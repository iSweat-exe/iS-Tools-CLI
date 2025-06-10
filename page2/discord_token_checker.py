#!/usr/bin/env python3
# coding: utf-8

import requests
import os
import time
import shutil

# Couleurs ANSI 256
PURPLE_VERY_LIGHT = '\033[38;5;201m'
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE = '\033[38;5;15m'
RED = '\033[38;5;196m'
GREEN = '\033[38;5;82m'
BOLD = '\033[1m'
RESET = '\033[0m'

ASCII_ART = r"""
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                   
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                 
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                 
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                  
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                     
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@                         
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((terminal_width - len(line)) // 2, 0)
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.02)

def print_centered(text):
    width = shutil.get_terminal_size((80, 20)).columns
    for line in text.splitlines():
        print(line.center(width))

def fetch_user_data(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=7)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            print(f"{RED}[Erreur]{RESET} Token invalide ou expiré.")
        else:
            print(f"{RED}[Erreur]{RESET} Code HTTP inattendu : {r.status_code}")
    except requests.RequestException as e:
        print(f"{RED}[Erreur]{RESET} {e}")
    return None

def fetch_user_guilds(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=7)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def nitro_status(premium_type: int | None) -> str:
    match premium_type:
        case 1:  return "Nitro Classic"
        case 2:  return "Nitro"
        case 3:  return "Nitro Basic"
        case _:  return "None"

def accent_to_hex(accent: int | None) -> str:
    return f"#{accent:06X}" if accent else "None"

def format_badges(flags):
    badge_map = {
        1 << 0: "Discord Employee",
        1 << 1: "Partnered Server Owner",
        1 << 2: "HypeSquad Events",
        1 << 3: "Bug Hunter Level 1",
        1 << 6: "House Bravery",
        1 << 7: "House Brilliance",
        1 << 8: "House Balance",
        1 << 9: "Early Supporter",
        1 << 14: "Bug Hunter Level 2",
        1 << 17: "Verified Bot Developer",
    }
    badges = [name for bit, name in badge_map.items() if flags & bit]
    return badges if badges else ["None"]

def print_user_info(data: dict, token: str):
    print(f"{PURPLE_LIGHT}{BOLD}┌────────────────────────────────────── {WHITE}Discord User Info{PURPLE_LIGHT}{BOLD} ──────────────────────────────────────┐{RESET}")

    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} User ID       : {WHITE}{data.get('id')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Phone Number  : {WHITE}{data.get('phone', 'None')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Email         : {WHITE}{data.get('email', 'None')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Global Name   : {WHITE}{data.get('global_name', 'None')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Verified      : {WHITE}{data.get('verified', False)}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} MFA           : {WHITE}{data.get('mfa_enabled', False)}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Locale        : {WHITE}{data.get('locale', 'None')}{RESET}")

    nitro = nitro_status(data.get('premium_type'))
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Nitro         : {WHITE}{nitro}{RESET}")

    accent = accent_to_hex(data.get('accent_color'))
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Accent Color  : {WHITE}{accent}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Token         : {WHITE}{token}{RESET}")

    print(f"{PURPLE_LIGHT}└────────────────────────────────────────────────────────────────────────────────────────────────┘{RESET}")

def run():
    clear_screen()
    print_ascii_art()
    print()

    while True:
        token = input(f"{PURPLE_LIGHT}Entrez un token Discord (ou 'q' pour quitter) : {RESET}").strip()
        if token.lower() in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break

        user_data = fetch_user_data(token)
        if user_data is None:
            continue

        print_user_info(user_data, token)

        guilds = fetch_user_guilds(token)
        if guilds:
            print(f"{PURPLE_LIGHT}{BOLD}┌─────────────────────────────────── {WHITE}Serveurs du compte ({len(guilds)}){PURPLE_LIGHT}{BOLD} ────────────────────────────────────┐{RESET}")
            
            max_name_length = 32  # Ajustable selon la taille du terminal

            # Trie les serveurs : admins d'abord, puis le reste par ordre alphabétique
            sorted_guilds = sorted(guilds, key=lambda g: (
                not bool(int(g.get("permissions", 0)) & 0x00000008),
                g.get("name", "").lower()
            ))

            for g in sorted_guilds:
                name = g.get("name", "Unknown")
                server_id = g.get("id", "N/A")
                admin = int(g.get("permissions", 0))
                is_admin = bool(admin & 0x00000008)

                # Tronque le nom s'il est trop long
                display_name = name if len(name) <= max_name_length else name[:max_name_length - 3] + "..."

                # Formate la ligne avec alignement
                line = f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} {display_name.ljust(max_name_length)}  ({WHITE}{server_id}{PURPLE_LIGHT})"
                if is_admin:
                    line += f"  {RED}[ADMIN]{RESET}"
                else:
                    line += RESET
                print(line)

            print(f"{PURPLE_LIGHT}└────────────────────────────────────────────────────────────────────────────────────────────────┘{RESET}")
            print()

if __name__ == "__main__":
    run()
