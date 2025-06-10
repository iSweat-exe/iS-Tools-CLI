import os
import sys
import shutil
from colorama import init, Fore, Style
from updater import check_and_update
import time

os.system("title iS-Tool Selector")

init(autoreset=True)

LINE_DELAY = 0.025

PASTEL_PINK = '\033[38;5;213m'  # Rose pastel
PASTEL_PURPLE = '\033[38;5;177m'  # Violet pastel
PURPLE_VERY_LIGHT = '\033[38;5;201m'  # Lavande très clair
PURPLE_LIGHT = '\033[38;5;177m'   # Lavande clair
PURPLE_NORMAL = '\033[38;5;129m'  # Violet standard
PURPLE_DARK = '\033[38;5;90m'     # Violet foncé
PURPLE_VERY_DARK = '\033[38;5;54m'    # Lavande très foncé

RED = '\033[38;5;196m'  # Rouge

# Autres couleurs et styles (ANSI 256)
WHITE = '\033[38;5;15m'
RESET = '\033[0m'
BOLD = '\033[1m'

def center_text(text):
    width = shutil.get_terminal_size((80, 20)).columns
    lines = text.splitlines()
    return "\n".join(line.center(width) for line in lines)

def print_with_loading(text, delay=0.01, color='', center=False):
    lines = text.splitlines()
    width = shutil.get_terminal_size((80, 20)).columns
    for line in lines:
        if center:
            print(f"{color}{line.center(width)}{RESET}", flush=True)
        else:
            print(f"{color}{line}{RESET}", flush=True)
        time.sleep(delay)

# Banner ASCII art
banner_art = r"""
 ██▓  ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▓██▒▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▒██▒░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
░██░  ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
░██░▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
░▓  ▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
 ▒ ░░ ░▒  ░ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
 ▒ ░░  ░  ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
 ░        ░                  ░ ░      ░ ░      ░  ░      ░  
"""

version = f"{WHITE}                    [Version : 1.0.0]{PURPLE_NORMAL}"

# Options textes
option_info_txt = f"{WHITE}Info {PURPLE_DARK}[{WHITE}26{PURPLE_NORMAL}]{PURPLE_NORMAL}"
option_next_txt = f"{WHITE}{PURPLE_DARK}[{WHITE}27{PURPLE_NORMAL}] {WHITE}Next{PURPLE_NORMAL}"
option_previous_txt = f"{WHITE}Previous {PURPLE_DARK}[{WHITE}28{PURPLE_NORMAL}]"
option_site_txt = f"{WHITE}Site{PURPLE_NORMAL}"
exit_option_txt = f"{PURPLE_DARK}[{WHITE}0{PURPLE_NORMAL}] {RED}Exit{PURPLE_NORMAL}"

option_01_txt = f"{PURPLE_DARK}[{WHITE}01{PURPLE_NORMAL}] {WHITE}IP Lookup{PURPLE_NORMAL}             "
option_02_txt = f"{PURPLE_DARK}[{WHITE}02{PURPLE_NORMAL}] {WHITE}IP Pinger{PURPLE_NORMAL}             "
option_03_txt = f"{PURPLE_DARK}[{WHITE}03{PURPLE_NORMAL}] {WHITE}IP Scanner{PURPLE_NORMAL}            "
option_04_txt = f"{PURPLE_DARK}[{WHITE}04{PURPLE_NORMAL}] {WHITE}Website Scanner{PURPLE_NORMAL}       "
option_05_txt = f"{PURPLE_DARK}[{WHITE}05{PURPLE_NORMAL}] {WHITE}Password Encrypted{PURPLE_NORMAL}    "
option_06_txt = f"{PURPLE_DARK}[{WHITE}06{PURPLE_NORMAL}] {WHITE}Password Decrypted{PURPLE_NORMAL}    "
option_07_txt = f"{PURPLE_DARK}[{WHITE}07{PURPLE_NORMAL}] {WHITE}Dox Creater{PURPLE_NORMAL}           "
option_08_txt = f"{PURPLE_DARK}[{WHITE}08{PURPLE_NORMAL}] {WHITE}EXIF Reader{PURPLE_NORMAL}           "
option_09_txt = f"{PURPLE_DARK}[{WHITE}09{PURPLE_NORMAL}] {WHITE}SQL Injection{PURPLE_NORMAL}         "
option_10_txt = f"{PURPLE_DARK}[{WHITE}10{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "

option_11_txt = f"{PURPLE_DARK}[{WHITE}11{PURPLE_NORMAL}] {WHITE}Discord Invite Info{PURPLE_NORMAL}   "
option_12_txt = f"{PURPLE_DARK}[{WHITE}12{PURPLE_NORMAL}] {WHITE}Discord Token Info{PURPLE_NORMAL}    "
option_13_txt = f"{PURPLE_DARK}[{WHITE}13{PURPLE_NORMAL}] {WHITE}Discord UserID Info{PURPLE_NORMAL}   "
option_14_txt = f"{PURPLE_DARK}[{WHITE}14{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_15_txt = f"{PURPLE_DARK}[{WHITE}15{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_16_txt = f"{PURPLE_DARK}[{WHITE}16{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_17_txt = f"{PURPLE_DARK}[{WHITE}17{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_18_txt = f"{PURPLE_DARK}[{WHITE}18{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_19_txt = f"{PURPLE_DARK}[{WHITE}19{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "

option_20_txt = f"{PURPLE_DARK}[{WHITE}20{PURPLE_NORMAL}] {WHITE}Password Checker{PURPLE_NORMAL}      "
option_21_txt = f"{PURPLE_DARK}[{WHITE}21{PURPLE_NORMAL}] {WHITE}Password Generator{PURPLE_NORMAL}    "
option_22_txt = f"{PURPLE_DARK}[{WHITE}22{PURPLE_NORMAL}] {WHITE}Crypto Wallet Checker{PURPLE_NORMAL} "
option_23_txt = f"{PURPLE_DARK}[{WHITE}23{PURPLE_NORMAL}] {WHITE}DVR Credentials{PURPLE_NORMAL}       "
option_24_txt = f"{PURPLE_DARK}[{WHITE}24{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_25_txt = f"{PURPLE_DARK}[{WHITE}25{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "

option_26_txt = f"{PURPLE_DARK}[{WHITE}26{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_27_txt = f"{PURPLE_DARK}[{WHITE}27{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_28_txt = f"{PURPLE_DARK}[{WHITE}28{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_29_txt = f"{PURPLE_DARK}[{WHITE}29{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_30_txt = f"{PURPLE_DARK}[{WHITE}30{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_31_txt = f"{PURPLE_DARK}[{WHITE}31{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_32_txt = f"{PURPLE_DARK}[{WHITE}32{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_33_txt = f"{PURPLE_DARK}[{WHITE}33{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_34_txt = f"{PURPLE_DARK}[{WHITE}34{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_35_txt = f"{PURPLE_DARK}[{WHITE}35{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "

option_36_txt = f"{PURPLE_DARK}[{WHITE}36{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_37_txt = f"{PURPLE_DARK}[{WHITE}37{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_38_txt = f"{PURPLE_DARK}[{WHITE}38{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_39_txt = f"{PURPLE_DARK}[{WHITE}39{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_40_txt = f"{PURPLE_DARK}[{WHITE}40{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_41_txt = f"{PURPLE_DARK}[{WHITE}41{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_42_txt = f"{PURPLE_DARK}[{WHITE}42{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_43_txt = f"{PURPLE_DARK}[{WHITE}43{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_44_txt = f"{PURPLE_DARK}[{WHITE}44{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_45_txt = f"{PURPLE_DARK}[{WHITE}45{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "

option_46_txt = f"{PURPLE_DARK}[{WHITE}46{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_47_txt = f"{PURPLE_DARK}[{WHITE}47{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_48_txt = f"{PURPLE_DARK}[{WHITE}48{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_49_txt = f"{PURPLE_DARK}[{WHITE}49{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_50_txt = f"{PURPLE_DARK}[{WHITE}50{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "
option_51_txt = f"{PURPLE_DARK}[{WHITE}51{PURPLE_NORMAL}] {WHITE}Comming Soon...{PURPLE_NORMAL}       "




menu_ascii_1 = f""" ┌─┤ {option_info_txt}                                                                                             {option_next_txt} ├─┐
 ├─┤ {option_site_txt}      ┌──────────────┐                          ┌──────────────┐                       ┌──────────────┐       │
 └─┬───────────┤    {WHITE}Page 1{PURPLE_NORMAL}    ├─────────────┬────────────┤    {WHITE}Page 2{PURPLE_NORMAL}    ├────────────┬──────────┤    {WHITE}Page 3{PURPLE_NORMAL}    ├───────┘
   │           └──────────────┘             │            └──────────────┘            │          └──────────────┘
   ├─ {option_01_txt}           ├─ {option_11_txt}           ├─ {option_20_txt}
   ├─ {option_02_txt}           ├─ {option_12_txt}           ├─ {option_21_txt}
   ├─ {option_03_txt}           ├─ {option_13_txt}           ├─ {option_22_txt}
   ├─ {option_04_txt}           ├─ {option_14_txt}           ├─ {option_23_txt}
   ├─ {option_05_txt}           ├─ {option_15_txt}           ├─ {option_24_txt}
   ├─ {option_06_txt}           ├─ {option_16_txt}           ├─ {option_25_txt}
   ├─ {option_07_txt}           ├─ {option_17_txt}           │
   ├─ {option_08_txt}           ├─ {option_18_txt}           │ 
   ├─ {option_09_txt}           ├─ {option_19_txt}           │        
   └─ {option_10_txt}           └─ {option_19_txt}           └─ {exit_option_txt}
{WHITE}
"""

menu_ascii_2 = f""" ┌─┤ {option_previous_txt}                                                                                         {option_next_txt} ├─┐
 ├─┤ {option_site_txt}      ┌──────────────┐                          ┌──────────────┐                       ┌──────────────┐       │
 └─┬───────────┤    {WHITE}Page 4{PURPLE_NORMAL}    ├─────────────┬────────────┤    {WHITE}Page 5{PURPLE_NORMAL}    ├────────────┬──────────┤    {WHITE}Page 6{PURPLE_NORMAL}    ├───────┘
   │           └──────────────┘             │            └──────────────┘            │          └──────────────┘
   ├─ {option_26_txt}           ├─ {option_36_txt}           ├─ {option_46_txt}
   ├─ {option_27_txt}           ├─ {option_37_txt}           ├─ {option_47_txt}
   ├─ {option_28_txt}           ├─ {option_38_txt}           ├─ {option_48_txt}
   ├─ {option_29_txt}           ├─ {option_39_txt}           ├─ {option_49_txt}
   ├─ {option_30_txt}           ├─ {option_40_txt}           ├─ {option_50_txt}
   ├─ {option_31_txt}           ├─ {option_41_txt}           ├─ {option_51_txt}
   ├─ {option_32_txt}           ├─ {option_42_txt}           │
   ├─ {option_33_txt}           ├─ {option_43_txt}           │ 
   ├─ {option_34_txt}           ├─ {option_44_txt}           │        
   └─ {option_35_txt}           └─ {option_45_txt}           └─ {exit_option_txt}
{WHITE}
"""

try:
    from page0 import info_software
    from page1 import ip_lookup, ip_pinger, ip_scanner, dox_create, get_image_exif, website_scanner, password_decrypted, password_encrypted, sql_injection, discord_server_info
    from page2 import discord_token_checker, discord_user_lookup
    from page3 import clipboardManager, cryptoWalletChecker, vpnProxyChecker, passwordGenerator, passwordStrengthChecker, cameraHacking
except ModuleNotFoundError as e:
    print(f"{Fore.RED}Erreur d'import : {e}")
    print("Assure-toi que tous les modules et dossiers nécessaires existent.")
    sys.exit(1)

def main():
    # Vérification et mise à jour du logiciel
    check_and_update(auto=True)
    current_page = 1
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print_with_loading(banner_art, delay=LINE_DELAY, color=PURPLE_VERY_LIGHT + BOLD, center=True)
        print()
        print_with_loading(version, delay=LINE_DELAY, color=PURPLE_NORMAL + BOLD, center=True)
        print("\n")
        if current_page == 1:
            print_with_loading(menu_ascii_1, delay=LINE_DELAY, color=PURPLE_NORMAL + BOLD)
        elif current_page == 2:
            print_with_loading(menu_ascii_2, delay=LINE_DELAY, color=PURPLE_NORMAL + BOLD)

        choice_input = input(f"{PASTEL_PURPLE}[iS-Tools Selector] -{RESET} {WHITE}Select a number : {RESET}")

        if not choice_input.isdigit():
            print(f"{Fore.RED}[iS-Tool Error] - Please enter a valid number.")
            time.sleep(1.5)
            continue

        choice = int(choice_input)

        # Navigation entre les pages
        if choice == 26: # Credits and Info
            info_software.run()
            continue
        elif choice == 27:  # Next
            if current_page < 2:
                current_page += 1
            else:
                print(f"{PASTEL_PURPLE}[iS-Tools Error] - {WHITE}You are already on the last page. Loading...{RESET}")
                time.sleep(1)
            continue
        elif choice == 28:  # Previous
            if current_page > 1:
                current_page -= 1
            else:
                print(f"{PASTEL_PURPLE}[iS-Tools Error] - {WHITE}You are already on the first page. Loading...{RESET}")
                time.sleep(1)
            continue
        elif choice == 0: # Exit
            print(f"{PASTEL_PURPLE}[iS-Tools] - {WHITE}Exiting the tool. Goodbye!{RESET}")
            sys.exit(0)


        # Page 1 options
        if choice == 1:
            ip_lookup.run()  # IP Tracker
        elif choice == 2:
            ip_pinger.run() # IP Pinger
        elif choice == 3:
            ip_scanner.run() # IP Scanner
        elif choice == 4:
            website_scanner.run() # Website Scanner
        elif choice == 5:
            password_encrypted.run() # Password Encrypted
        elif choice == 6:
            password_decrypted.run() # Password Decrypted
        elif choice == 7:
            dox_create.run() # Dox Creater
        elif choice == 8:
            get_image_exif.run() # EXIF Reader
        elif choice == 9:
            sql_injection.run() # SQL Injection
        elif choice == 10:
            print(f"{Fore.RED}[iS-Tool Error] - This option is not yet implemented.")

        # Page 2 options
        elif choice == 11:
            discord_server_info.run() # Discord Invite Info
        elif choice == 12:
            discord_token_checker.run() # Discord Token Info
        elif choice == 13:
            discord_user_lookup.run() # Discord UserID Info
        elif choice in range(14, 20):
            print(f"{Fore.RED}[iS-Tool Error] - This option is not yet implemented.")

        # Page 3 options
        elif choice == 20:
            passwordStrengthChecker.run() # Password Checker
        elif choice == 21:
            passwordGenerator.run() # Password Generator
        elif choice == 22:
            cryptoWalletChecker.run() # Crypto Wallet Checker
        elif choice == 23:
            cameraHacking.run() # Camera Hacking (CVE-2018-9995 DVR Credentials Exploit)

        # Options
        elif choice in range(24, 25):
            print(f"{Fore.RED}[iS-Tool Error] - This option is not yet implemented.")
        elif choice in range(29, 51):
            print(f"{Fore.RED}[iS-Tool Error] - This option is not yet implemented.")
        else:
            print(f"{Fore.RED}[iS-Tool Error] - Invalid choice.")

        input(f"\n{PASTEL_PURPLE}[iS-Tool Info] -{RESET} {WHITE}Appuie sur Entrée pour revenir au menu...{RESET}")
        os.system("title iS-Tool Selector")

if __name__ == "__main__":
    main()
