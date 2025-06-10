#!/usr/bin/env python3
# coding: utf-8

import requests
import re
import os
import time
import shutil

# Couleurs ANSI 256
PURPLE_VERY_LIGHT = '\033[38;5;201m'  # Lavande très clair
PURPLE_LIGHT = '\033[38;5;177m'       # Lavande clair
PURPLE_NORMAL = '\033[38;5;129m'      # Violet standard
PURPLE_DARK = '\033[38;5;90m'         # Violet foncé
WHITE = '\033[38;5;15m'
RED = '\033[38;5;196m'
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

def print_ascii_art():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((terminal_width - len(line)) // 2, 0)
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.02)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_code(invite_url):
    """
    Extrait le code d'invitation Discord depuis une URL.
    Exemples valides :
    - https://discord.gg/abcdef
    - discord.gg/abcdef
    - abcdef (juste le code)
    """
    pattern = re.compile(r'(?:https?://)?(?:www\.)?discord(?:app)?\.gg/([a-zA-Z0-9\-]+)')
    match = pattern.search(invite_url)
    if match:
        return match.group(1)
    # Si l'utilisateur rentre juste le code sans URL
    if re.match(r'^[a-zA-Z0-9\-]+$', invite_url):
        return invite_url
    return None

def fetch_invite_data(code):
    url = f"https://discord.com/api/v10/invites/{code}?with_counts=true&with_expiration=true"
    headers = {
        "User-Agent": "iS-Tool/1.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 404:
            print(f"{RED}[Erreur]{RESET} Invitation introuvable ou invalide.")
            return None
        if response.status_code != 200:
            print(f"{RED}[Erreur]{RESET} Code HTTP inattendu : {response.status_code}")
            return None
        return response.json()
    except requests.RequestException as e:
        print(f"{RED}[Erreur]{RESET} {e}")
        return None

def safe_get(d, key, default="None"):
    val = d.get(key, default)
    if val is None:
        return default
    return val

def print_invite_info(data, code):
    print(f"{PURPLE_LIGHT}{BOLD}┌───────────── Invitation Information ─────────────┐{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Invitation         : {WHITE}https://discord.gg/{code}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Type               : {WHITE}{safe_get(data, 'type')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Code               : {WHITE}{code}{RESET}")

    expired = safe_get(data, 'expires_at')
    if expired is None:
        expired = "None"
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Expired            : {WHITE}{expired}{RESET}")

    guild = safe_get(data, 'guild', {})
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server ID          : {WHITE}{safe_get(guild, 'id')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Name        : {WHITE}{safe_get(guild, 'name')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Description : {WHITE}{safe_get(guild, 'description', 'None')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Icon        : {WHITE}{safe_get(guild, 'icon', 'None')}{RESET}")

    features = safe_get(guild, 'features', [])
    features_str = " / ".join(features) if features else "None"
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Features    : {WHITE}{features_str}{RESET}")

    nsfw_level = safe_get(guild, 'nsfw_level', 0)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server NSFW Level  : {WHITE}{nsfw_level}{RESET}")
    nsfw = safe_get(guild, 'nsfw', False)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server NSFW        : {WHITE}{nsfw}{RESET}")

    flags = safe_get(guild, 'flags', 0)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Flags              : {WHITE}{flags}{RESET}")

    verification_level = safe_get(guild, 'verification_level', 0)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Verification Level         : {WHITE}{verification_level}{RESET}")

    premium_sub_count = safe_get(guild, 'premium_subscription_count', 0)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Server Premium Subscription Count : {WHITE}{premium_sub_count}{RESET}")
    print(f"{PURPLE_LIGHT}{BOLD}└──────────────────────────────────────────────────┘{RESET}")

    channel = safe_get(data, 'channel', {})
    print(f"\n{PURPLE_LIGHT}{BOLD}┌────────────── Channel Information ────────────────┐{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Channel ID         : {WHITE}{safe_get(channel, 'id')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Channel Name       : {WHITE}{safe_get(channel, 'name')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Channel Type       : {WHITE}{safe_get(channel, 'type')}{RESET}")
    print(f"{PURPLE_LIGHT}{BOLD}└───────────────────────────────────────────────────┘{RESET}")


    inviter = safe_get(data, 'inviter', None)
    if inviter:
        print(f"\n{PURPLE_LIGHT}{BOLD}┌─────────────────── Inviter Information ───────────────────┐{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} ID            : {WHITE}{safe_get(inviter, 'id')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Username      : {WHITE}{safe_get(inviter, 'username')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Global Name   : {WHITE}{safe_get(inviter, 'global_name', 'None')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Avatar        : {WHITE}{safe_get(inviter, 'avatar')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Discriminator : {WHITE}{safe_get(inviter, 'discriminator')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Public Flags  : {WHITE}{safe_get(inviter, 'public_flags')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Flags         : {WHITE}{safe_get(inviter, 'flags')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Banner        : {WHITE}{safe_get(inviter, 'banner', 'None')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Accent Color  : {WHITE}{safe_get(inviter, 'accent_color', 'None')}{RESET}")
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Banner Color  : {WHITE}{safe_get(inviter, 'banner_color', 'None')}{RESET}")
        print(f"{PURPLE_LIGHT}{BOLD}└───────────────────────────────────────────────────────────┘{RESET}")
    else:
        print(f"\n{RED}[Info]{RESET} Pas d'inviteur trouvé pour cette invitation.")

def run():
    clear_screen()
    os.system("title iS-Tools - Discord Invite Info" if os.name == 'nt' else '')
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}===== Discord Invite Info - Tapez 'q' ou 'quit' pour quitter ====={RESET}")

    while True:
        invite_input = input(f"{PURPLE_LIGHT}[Discord Invite] -{RESET} Entrez une invitation Discord : ").strip()
        if invite_input.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            print()
            break

        code = extract_code(invite_input)
        if not code:
            print(f"{RED}[Erreur]{RESET} URL ou code d'invitation Discord invalide.")
            continue

        data = fetch_invite_data(code)
        if data is None:
            continue

        print()
        print_invite_info(data, code)
        print()

if __name__ == "__main__":
    run()
