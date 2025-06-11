# coding: utf-8

# ─────────── Imports ───────────
import hashlib, base64, bcrypt, sys, time, shutil, os

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
                                     p@@@j         ;@@@@^                      """

# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    term_w = shutil.get_terminal_size((80, 20)).columns
    for ln in ASCII_ART.strip('\n').splitlines():
        pad = max((term_w - len(ln)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + ln + RESET)
        time.sleep(0.02)

# ─── Fonctions de chiffrement ─────────────────────────────────────────────────
def encrypt_password(method: str, password: str) -> str:
    match method:
        case "1":  # BCRYPT
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            return hashed.decode()
        case "2":  # MD5
            return hashlib.md5(password.encode()).hexdigest()
        case "3":  # SHA-1
            return hashlib.sha1(password.encode()).hexdigest()
        case "4":  # SHA-256
            return hashlib.sha256(password.encode()).hexdigest()
        case "5":  # PBKDF2
            salt = b"iS-Tool"
            dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
            return dk.hex()
        case "6":  # Base64
            return base64.b64encode(password.encode()).decode()
        case _:
            return ""

# ─── Menu principal ──────────────────────────────────────────────────────────
def print_menu():
    print(f"{PURPLE_LIGHT}===== Password Encrypted - tapez 'q' pour quitter ====={RESET}\n")
    print(f"\n{PURPLE_LIGHT}{BOLD}┌───── [ENCRYPTATION METHOD] ─────┐{RESET}")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}01{WHITE}] BCRYPT")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}02{WHITE}] MD5")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}03{WHITE}] SHA-1")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}04{WHITE}] SHA-256")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}05{WHITE}] PBKDF 2")
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}06{WHITE}] Base64 Encode")
    print(f"{PURPLE_LIGHT}{BOLD}└─────────────────────────────────┘{RESET}\n")
    print()

# ─── Point d’entrée ──────────────────────────────────────────────────────────
def run():
    clear_screen()
    os.system("title iS-Tools - Password Encrypted") 
    print_ascii_art()
    print_menu()
    while True:
        method = input(f"{PURPLE_LIGHT}[Password Encrypted] -{RESET} Encryptation Method : ").strip().lower()
        if method in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break
        if method not in ("1", "2", "3", "4", "5", "6"):
            print(f"{WHITE}[{PURPLE_LIGHT}!{WHITE}]{PURPLE_LIGHT} Méthode invalide.{RESET}\n")
            continue
        password = input(f"{PURPLE_LIGHT}[Password Encrypted] -{RESET} Password to Encrypt : ")
        result = encrypt_password(method, password)
        print(f"{PURPLE_LIGHT}[Password Encrypted] -{RESET} Encrypted Password : {WHITE}{result}{RESET}\n")

# ─── Exécution directe ────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterruption par l’utilisateur.")
        sys.exit(0)
