#!/usr/bin/env python3
# coding: utf-8

# ─────────── Imports ───────────
import base64, sys, time, shutil, os

# ─────────── Couleurs ANSI 256 ───────────
PASTEL_PINK = '\033[38;5;213m'
PASTEL_PURPLE = '\033[38;5;177m'
PURPLE_VERY_LIGHT = '\033[38;5;201m'
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
PURPLE_DARK = '\033[38;5;90m'
PURPLE_VERY_DARK = '\033[38;5;54m'
RED = '\033[38;5;196m'
WHITE = '\033[38;5;15m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ─────────── ASCII Art ─────────
ASCII_ART = r"""
                                         ^M@@@@@@@@@v                                    
                                      v@@@@@@@@@@@@@@@@@                                 
                                    _@@@@@@@}    ;a@@@@@@@                               
                                   M@@@@@            @@@@@@                              
                                  ;@@@@@              O@@@@@                             
                                  @@@@@v               @@@@@                             
                                  @@@@@;               @@@@@                             
                                  @@@@@;                                                 
                                  @@@@@;        v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@j     @@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@v       @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@_   @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|      
                                               ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@O  """

# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    term_w = shutil.get_terminal_size((80, 20)).columns
    for ln in ASCII_ART.strip('\n').splitlines():
        pad = max((term_w - len(ln)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + ln + RESET)
        time.sleep(0.02)

# ─── Fonctions de déchiffrement ───────────────────────────────────────────────
def decrypt_password(method: str, encrypted: str) -> str:
    if method == "6":  # Base64
        try:
            decoded_bytes = base64.b64decode(encrypted)
            return decoded_bytes.decode()
        except Exception:
            return f"{RED}Erreur: chaîne Base64 invalide ou illisible.{RESET}"
    else:
        return f"{RED}Erreur: méthode non réversible (décryptage impossible).{RESET}"

# ─── Menu principal ──────────────────────────────────────────────────────────
def print_menu():
    print(f"{PURPLE_LIGHT}===== Password Decrypted - tapez 'q' pour quitter ====={RESET}\n")
    print(f"{PURPLE_DARK}[{WHITE}01{PURPLE_NORMAL}] {WHITE}BCRYPT (NON RÉVERSIBLE)")
    print(f"{PURPLE_DARK}[{WHITE}02{PURPLE_NORMAL}] {WHITE}MD5 (NON RÉVERSIBLE)")
    print(f"{PURPLE_DARK}[{WHITE}03{PURPLE_NORMAL}] {WHITE}SHA-1 (NON RÉVERSIBLE)")
    print(f"{PURPLE_DARK}[{WHITE}04{PURPLE_NORMAL}] {WHITE}SHA-256 (NON RÉVERSIBLE)")
    print(f"{PURPLE_DARK}[{WHITE}05{PURPLE_NORMAL}] {WHITE}PBKDF 2 (NON RÉVERSIBLE)")
    print(f"{PURPLE_DARK}[{WHITE}06{PURPLE_NORMAL}] {WHITE}Base64 Decode")
    print()

# ─── Point d’entrée ──────────────────────────────────────────────────────────
def run():
    clear_screen()
    os.system("title iS-Tools - Password Decrypted") 
    print_ascii_art()
    print_menu()
    while True:
        method = input(f"{PURPLE_LIGHT}[Password Decrypted] -{RESET} Decryptation Method : ").strip().lower()
        if method in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break
        if method not in ("1", "2", "3", "4", "5", "6"):
            print(f"{WHITE}[{PURPLE_LIGHT}!{WHITE}]{PURPLE_LIGHT} Méthode invalide.{RESET}\n")
            continue
        encrypted = input(f"{PURPLE_LIGHT}[Password Decrypted] -{RESET} Password to Decrypt : ")
        result = decrypt_password(method, encrypted)
        print(f"{PURPLE_LIGHT}[Password Decrypted] -{RESET} Decrypted Password : {WHITE}{result}{RESET}\n")

# ─── Exécution directe ────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterruption par l’utilisateur.")
        sys.exit(0)
