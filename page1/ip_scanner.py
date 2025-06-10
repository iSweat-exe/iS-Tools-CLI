#!/usr/bin/env python3
# coding: utf-8

import subprocess
import platform
import re
import time
import ipaddress
import shutil 
import os

# Couleurs ANSI 256
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE = '\033[38;5;15m'
GREEN = '\033[38;5;46m'
RED = '\033[38;5;196m'
RESET = '\033[0m'

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
    """Ping une IP une fois, retourne True si OK, sinon False"""
    system = platform.system().lower()
    if system == 'windows':
        cmd = ['ping', '-n', '1', '-w', '1000', ip]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', ip]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except Exception:
        return False

def run():
    clear_screen()
    os.system("title iS-Tools - IP Scanner") 
    print()
    print_ascii_art()
    print(f"{PURPLE_LIGHT}===== IP Scanner - Tapez 'q' ou 'quit' pour quitter ====={RESET}")
    while True:
        plage = input(f"{PURPLE_LIGHT}[IP Scanner] -{RESET} Entrez la plage IP (exemple 192.168.1.1-192.168.1.20) : ").strip()
        if plage.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break

        try:
            start_ip, end_ip = plage.split('-')
            if not is_valid_ip(start_ip) or not is_valid_ip(end_ip):
                print(f"{RED}[Erreur]{RESET} Format d'IP invalide.")
                continue
            start_int = int(ipaddress.IPv4Address(start_ip))
            end_int = int(ipaddress.IPv4Address(end_ip))
            if start_int > end_int:
                print(f"{RED}[Erreur]{RESET} La première IP doit être inférieure à la deuxième.")
                continue
        except Exception:
            print(f"{RED}[Erreur]{RESET} Format de plage invalide, exemple attendu : 192.168.1.1-192.168.1.20")
            continue
        print()

        print(f"{PURPLE_NORMAL}[IP Scanner] -{WHITE} Scan en cours de {start_ip} à {end_ip}...{RESET}")
        for ip_int in range(start_int, end_int + 1):
            ip = str(ipaddress.IPv4Address(ip_int))
            if ping_once(ip):
                print(f"{GREEN}[IP Scanner] -{WHITE} IP active : {ip}{RESET}")
        print(f"{PURPLE_LIGHT}[IP Scanner] -{RESET} Scan terminé.\n")

if __name__ == "__main__":
    run()
