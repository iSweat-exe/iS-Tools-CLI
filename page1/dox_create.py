#!/usr/bin/env python3
# coding: utf-8

import os
import time
import shutil
from datetime import datetime

# Couleurs ANSI 256 (repris du IP Tracker)
PURPLE_VERY_LIGHT = '\033[38;5;201m'
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
PURPLE_DARK = '\033[38;5;90m'
WHITE = '\033[38;5;15m'
GREEN = '\033[38;5;46m'
RESET = '\033[0m'

ASCII_ART = r"""                                            
                  .:+*#%%#####*++++-.             
                :#%%*+*+-.....                    
             .=%%+++:..                           
           .=%#++=.                               
          -%%+++.                                 
      .  =%%++-          ....                     
      #%+#%++=.        .:#%%%*:                   
      :#@%#+=          :*+:-*%#:                  
       .*@@#.         .-%*::-%%#.                 
        .-%@@%-.      .=%%--%%%-                  
                         .:--=*+-:.:-#%%%%%%%%*.                      ██████╗   ██████╗  ██╗  ██╗
                              .:-*#%%%%%%%%%%%%%-                     ██╔══██╗ ██╔═══██╗ ╚██╗██╔╝
                                 .+%%%*+*%%%%%%%%+...                 ██║  ██║ ██║   ██║  ╚███╔╝ 
                                 .+%@@%%%%*#%%%%%%%%%*-.              ██║  ██║ ██║   ██║  ██╔██╗
                                  .*%@%%%%%%%%%%%%%%%%%#-.            ██████╔╝ ╚██████╔╝ ██╔╝ ██╗
                                  .*%%%%%%%%%%%+#%%%%%%%%%*-.         ╚═════╝   ╚═════╝  ╚═╝  ╚═╝
                  .=%%%%%%%%%%%%@%*%%%%%####=-==  
                                  :*%%%%%%%%%%%%%%%*#%%%%#+=-==+      iS-Tool - Dox Creator.
                 .+=*%#%%%%%%%%%%%%%**%%#+**+-:-  
                .-=::*-%%%%%%%%%%%%###*-*%###+:   
                ...:..%%%%%%%%%%%%%%#:=*+-:.      
                     *%%%%%%%%%%%%%%%%.           
                    :#%%%%%%%%%%%%%%%%+           
                   .*%%%%%%%%%%%%%%%%%#.          
                  .=%%%%%%%%%%%%%%%%%%#:          
                  .+%%%%%%%%%%%%%%%%%%%*.         
                    :+*#%%%@%%%%%%%%%%%%#:.       
                      ..:==+*#%#*=-:.:-+***:."""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((terminal_width - len(line)) // 2 - 20, 0) # 20 Left padding
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.025)

def get_input(prompt):
    try:
        return input(f"{PURPLE_LIGHT}[Dox Creator] -{RESET} {prompt} ").strip()
    except KeyboardInterrupt:
        print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
        exit()

def run():
    clear_screen()
    os.system("title iS-Tools - Dox Creator") 
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}===== DOX CREATOR - Tapez 'q' ou 'quit' pour quitter ====={RESET}\n")

    pseudo = get_input("Pseudo :")
    nom = get_input("Nom :")
    prenom = get_input("Prénom :")
    age = get_input("Âge :")
    adresse = get_input("Adresse :")
    email = get_input("Email :")
    telephone = get_input("Numéro de téléphone :")
    ip = get_input("Adresse IP (optionnel) :")

    twitter = get_input("Twitter :")
    instagram = get_input("Instagram :")
    youtube = get_input("YouTube :")
    tiktok = get_input("TikTok :")
    facebook = get_input("Facebook :")
    snapchat = get_input("Snapchat :")

    filename = f"{pseudo or prenom or 'dox'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_path = os.path.join(os.getcwd(), filename)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("====== DOX INFORMATION ======")
        f.write(f"Pseudo     : {pseudo}\n")
        f.write(f"Nom        : {nom}\n")
        f.write(f"Prénom     : {prenom}\n")
        f.write(f"Âge        : {age}\n")
        f.write(f"Adresse    : {adresse}\n")
        f.write(f"Email      : {email}\n")
        f.write(f"Téléphone  : {telephone}\n")
        f.write(f"Adresse IP : {ip}\n")
        f.write("\n--- Réseaux Sociaux ---")
        f.write(f"Twitter    : {twitter}\n")
        f.write(f"Instagram  : {instagram}\n")
        f.write(f"YouTube    : {youtube}\n")
        f.write(f"TikTok     : {tiktok}\n")
        f.write(f"Facebook   : {facebook}\n")
        f.write(f"Snapchat   : {snapchat}\n")
        f.write("==============================\n")

    print(f"\n{GREEN}[Dox Creator Saver]{RESET} Fichier sauvegardé sous : {WHITE}{filename}{RESET}\n")

if __name__ == "__main__":
    run()
