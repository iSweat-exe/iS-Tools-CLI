#!/usr/bin/env python3
# coding: utf-8

import subprocess
import platform
import re
import time
import shutil  # <- pour la taille du terminal
import os

# Couleurs ANSI 256
PURPLE_LIGHT = '\033[38;5;177m'       # Lavande clair
PURPLE_NORMAL = '\033[38;5;129m'      # Violet standard
WHITE = '\033[38;5;15m'
GREEN = '\033[38;5;46m'
RED = '\033[38;5;196m'
YELLOW = '\033[38;5;226m'
RESET = '\033[0m'
BOLD = '\033[1m'

ASCII_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                    ⠀
                         :**+ :::+*@@.                                                       
                 +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -                    
    @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:        
.#@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*      
#*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=       
      *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.      
      #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=          
     @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%@@@@@@@@@@@@@@@@@=  +        
    :@@@@@@@@@@@@@@:                   :@@    # - @@@@@@@ =@@@*#*@@@@@@@@@@@@@=.=-  #:       
     :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@             
      #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:            
        @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==            
        =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :           
            .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=              
               . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.         
                :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=            
               -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :     
                @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.  
                 @@@@@@@@@@@@@                #@@@@@@%@.                             :  :    
                  *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .@@@@=:@    
                   :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@   
                   :@@@@%@@                   .@@@@@-   .                     @@@@@@@@@@@@*  
                   :@@@@%@@                    *@@@-                          @@@@@@@@@@@@  
                   :@@@@%@@                                                        =@@@:    @=
                    =@@                                                              =    #+ 
                     @%                                                                        
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─── Impression centrée, ligne par ligne (animation) ─────────────────────────
def print_ascii_art():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((terminal_width - len(line)) // 2, 0)
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.025)          # garde l’animation « ligne par ligne »

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True

def ping_once(ip):
    system = platform.system().lower()
    if system == 'windows':
        cmd = ['ping', '-n', '1', ip]
    else:
        cmd = ['ping', '-c', '1', ip]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout

        if result.returncode != 0:
            return None

        if system == 'windows':
            match = re.search(r'octets=(\d+)\s+temps=(\d+)\s*ms\s+TTL=(\d+)', output, re.IGNORECASE)
            if match:
                octets, temps, ttl = match.groups()
            else:
                return None
        else:
            match = re.search(r'(\d+) bytes from .* ttl=(\d+) time=(\d+\.?\d*) ms', output, re.IGNORECASE)
            if match:
                octets, ttl, temps = match.groups()
            else:
                return None

        return {
            'octets': octets,
            'temps': temps,
            'ttl': ttl,
            'code': 200
        }
    except Exception:
        return None

def run():
    clear_screen()
    os.system("title iS-Tools - IP Pinger")
    print()
    print_ascii_art()
    print(f"{PURPLE_LIGHT}===== IP Pinger - Tapez 'q' ou 'quit' pour quitter ====={RESET}")
    
    while True:
        target = input(f"{PURPLE_LIGHT}[IP Pinger] -{RESET} Entrez l'adresse IP à PING : ").strip()
        if target.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break
        if not is_valid_ip(target):
            print(f"{RED}[Erreur]{RESET} Adresse IP invalide.")
            continue

        ping_input = input(f"{PURPLE_LIGHT}[IP Pinger] -{RESET} Nombre de pings (par défaut 5) : ").strip()
        try:
            number_of_pings = int(ping_input) if ping_input else 5
        except ValueError:
            print(f"{PURPLE_LIGHT}[IP Pinger Error] -{RESET} Entrée invalide. Nombre de pings réglé sur 5 par défaut.")
            number_of_pings = 5

        print()
        print(f"{PURPLE_LIGHT}{BOLD}┌───────────────────────────────────── [IP PINGER] ─────────────────────────────────────┐{RESET}")
        for i in range(number_of_pings):
            res = ping_once(target)
            if res:
                print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] {PURPLE_LIGHT}[IP Pinger] -{WHITE} Réponse de {target} | "
                      f"{res['octets']} octets | {res['temps']} ms | TTL: {res['ttl']} | {GREEN}OK {res['code']}{RESET}")
            else:
                print(f"{PURPLE_LIGHT}├─ {WHITE}[{RED}X{WHITE}] {RED}[IP Pinger] -{RESET} Aucun retour ou erreur lors du ping vers {target}.")
            time.sleep(1)
        print(f"{PURPLE_LIGHT}{BOLD}└───────────────────────────────────────────────────────────────────────────────────────┘{RESET}")
        print()

if __name__ == "__main__":
    run()
