#!/usr/bin/env python3
# coding: utf-8

import os, shutil, time, random

PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
RED           = '\033[38;5;196m'
GREEN         = '\033[38;5;82m'
BOLD          = '\033[1m'
RESET         = '\033[0m'

ASCII_ART = r"""
                                               j@@@@@^                                 
           _@v   p@@@@j           j@@@@@@@@@@@@@@@;          |@@@@M   v@}      
          @@@@@} >@@@@    v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@p    @@@@_ _@@@@@     
          >@@@v    @@     v@@@@@@@@@@@@      p@@@@@@@@@@@a     @@    j@@@_     
           ^@@     @@@@   |@@@@@@@@@@^ @@@@@@; @@@@@@@@@@p   p@@@     M@;      
           ^@@            >@@@@@@@@@@ p@@@@@@@ M@@@@@@@@@j            M@;      
           ^@@@@@@@@@@@}   @@@@@@@@|            >@@@@@@@@;   @@@@@@@@@@@;      
                           }@@@@@@@|    O@@@    >@@@@@@@M                      
          |@@@@             @@@@@@@|     M@     >@@@@@@@^            @@@@j     
          @@@@@@@@@@@@@@@>   @@@@@@|    O@@@    >@@@@@@    @@@@@@@@@@@@@@@     
            ^                 @@@@@v            }@@@@@^                ^       
                 p@@@@@@@@@^   M@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@p            
                 p@_            ^@@@@@@@@@@@@@@@@@@>            >@a            
                @@@@O              @@@@@@@@@@@@@@              J@@@@           
               ;@@@@@                 J@@@@@@p                 @@@@@>          
                  ;              p@              p@>  M@@_       ;             
                          @@@@p  p@_  ;      j_  a@@@@@@@@j                    
                         ^@@@@@@@@@   v@_   O@}       M@@_                     
                            ;         p@|   O@}      }}                        
                                    >@@@@@  O@@@@@@@@@@@J                      
                                     p@@@j         ;@@@@^                     
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip("\n").splitlines():
        pad = max((width - len(line)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + line + RESET)
        time.sleep(0.01)

def ask_int(prompt, min_value, max_value, default=None):
    while True:
        try:
            res = input(f"{PURPLE_LIGHT}{prompt} [{min_value}-{max_value}]{(' (défaut '+str(default)+')' if default else '')}: {RESET}")
            if res.strip() == "" and default is not None:
                return default
            val = int(res)
            if min_value <= val <= max_value:
                return val
            else:
                print(f"{RED}Erreur: entrez un nombre entre {min_value} et {max_value}.{RESET}")
        except ValueError:
            print(f"{RED}Erreur: entrez un nombre valide.{RESET}")

def ask_yes_no(prompt, default="y"):
    yes = {"y","yes","o","oui"}
    no = {"n","no","non"}
    while True:
        res = input(f"{PURPLE_LIGHT}{prompt} (Y/n): {RESET}").strip().lower()
        if res == "" and default is not None:
            return default in yes
        if res in yes:
            return True
        if res in no:
            return False
        print(f"{RED}Répondez par oui ou non (y/n).{RESET}")

def get_character_sets():
    return {
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "symbols": "!@#$%^&*()_-+=[]{}|;:'\",.<>?/`~"
    }

def suggest_best_security():
    print(f"\n{GREEN}{BOLD}Recommandation de sécurité :{RESET}")
    print(f"{GREEN}Pour un mot de passe vraiment sûr, utilisez au minimum :")
    print(" - Lettres minuscules + majuscules")
    print(" - Chiffres")
    print(" - Caractères spéciaux (symboles)")
    print(f"Et une longueur d'au moins 12 caractères.{RESET}\n")

def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    sets = get_character_sets()
    pool = ""
    if use_lower:  pool += sets["lower"]
    if use_upper:  pool += sets["upper"]
    if use_digits: pool += sets["digits"]
    if use_symbols:pool += sets["symbols"]
    if not pool:
        return None

    pwd = []
    if use_lower:  pwd.append(random.choice(sets["lower"]))
    if use_upper:  pwd.append(random.choice(sets["upper"]))
    if use_digits: pwd.append(random.choice(sets["digits"]))
    if use_symbols:pwd.append(random.choice(sets["symbols"]))

    while len(pwd) < length:
        pwd.append(random.choice(pool))

    random.shuffle(pwd)
    return "".join(pwd[:length])

def print_password_info(count, length, use_lower, use_upper, use_digits, use_symbols):
    label_w = 35
    print(f"{PURPLE_LIGHT}{BOLD}┌───────────── [ Password Informations ] ─────────────┐{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] Nombre de mot de passe généré".ljust(label_w)+f": {WHITE}{count}{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] Longueur".ljust(label_w)+f": {WHITE}{length}{RESET}")
    types = []
    if use_lower: types.append("minuscules")
    if use_upper: types.append("majuscules")
    if use_digits: types.append("chiffres")
    if use_symbols: types.append("symboles")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] Types inclus".ljust(label_w)+f": {WHITE}{', '.join(types) if types else 'Aucun'}{RESET}")
    print(f"{PURPLE_LIGHT}└{'─'*(53)}┘{RESET}")

def print_passwords(passwords):
    label_w = 25
    print(f"{PURPLE_LIGHT}{BOLD}┌────────────────── [ Mot de passe ] ─────────────────┐{RESET}")
    for i, pwd in enumerate(passwords, 1):
        label = f"Mot de passe généré ({i})"
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] {label.ljust(label_w)}: {WHITE}{pwd}{RESET}")
    print(f"{PURPLE_LIGHT}└{'─'*(53)}┘{RESET}")

def run():
    clear()
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}===== Password Generator – tapez 'q' pour quitter ====={RESET}\n")

    while True:
        length = ask_int("Longueur du mot de passe", 6, 128, default=16)
        use_lower = ask_yes_no("Inclure lettres minuscules (a-z) ?", default="y")
        use_upper = ask_yes_no("Inclure lettres majuscules (A-Z) ?", default="y")
        use_digits = ask_yes_no("Inclure chiffres (0-9) ?", default="y")
        use_symbols = ask_yes_no("Inclure symboles spéciaux (ex: !@#$...) ?", default="y")

        if not (use_lower and use_upper and use_digits and use_symbols):
            suggest_best_security()

        if not (use_lower or use_upper or use_digits or use_symbols):
            print(f"{RED}Erreur: vous devez choisir au moins un type de caractère.{RESET}\n")
            continue

        count = ask_int("Combien de mots de passe générer ?", 1, 100, default=5)

        print()
        passwords = []
        for _ in range(count):
            pwd = generate_password(length, use_lower, use_upper, use_digits, use_symbols)
            if pwd is None:
                print(f"{RED}Erreur: pas de caractères sélectionnés.{RESET}")
                break
            passwords.append(pwd)

        print_password_info(count, length, use_lower, use_upper, use_digits, use_symbols)
        print_passwords(passwords)

        print()
        if not ask_yes_no("Voulez-vous générer un autre mot de passe ?", default="y"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break
        print()

if __name__ == "__main__":
    run()
