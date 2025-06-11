# coding: utf-8

# ─────────── Imports ───────────
import os, shutil, time, re, math

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
RED           = '\033[38;5;196m'
BOLD          = '\033[1m'
RESET         = '\033[0m'

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

# ─────────── Utils écriture CLI ─────────
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip("\n").splitlines():
        pad = max((width - len(line)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + line + RESET)
        time.sleep(0.02)

def entropy_label(bits):
    if bits < 28:  return "Très faible"
    if bits < 36:  return "Faible"
    if bits < 60:  return "Moyenne"
    if bits < 128: return "Forte"
    return "Très forte"

def is_repeated_substring(pwd):
    length = len(pwd)
    for size in range(1, length // 2 + 1):
        if length % size == 0:
            sub = pwd[:size]
            if sub * (length // size) == pwd:
                return True
    return False

def has_sequential_chars(pwd, seq_len=4):
    pwd_lower = pwd.lower()
    for i in range(len(pwd_lower) - seq_len + 1):
        segment = pwd_lower[i:i+seq_len]
        # Check ascending
        if all(ord(segment[j]) + 1 == ord(segment[j+1]) for j in range(seq_len-1)):
            return True
        # Check descending
        if all(ord(segment[j]) - 1 == ord(segment[j+1]) for j in range(seq_len-1)):
            return True
    return False

def character_pool_size(classes):
    pool = 0
    pool += 26 if classes["lower"] else 0
    pool += 26 if classes["upper"] else 0
    pool += 10 if classes["digit"] else 0
    pool += len("!@#$%^&*()_-+=[]{}|;:'\",.<>?/`~") if classes["symb"] else 0
    return pool

def seconds_to_human(sec):
    units = [
        ("trillions d'années", 1e12 * 365.25 * 24 * 3600),
        ("milliards d'années", 1e9 * 365.25 * 24 * 3600),
        ("millions d'années", 1e6 * 365.25 * 24 * 3600),
        ("milliers d'années", 1e3 * 365.25 * 24 * 3600),
        ("années", 365.25 * 24 * 3600),
        ("mois", 30.44 * 24 * 3600),
        ("semaines", 7 * 24 * 3600),
        ("jours", 24 * 3600),
        ("heures", 3600),
        ("minutes", 60),
        ("secondes", 1),
    ]

    for name, count in units:
        if sec >= count:
            val = sec / count
            val_str = f"{val:.2f}" if not val.is_integer() else f"{int(val)}"
            return f"{val_str} {name}"
    return "moins d'une seconde"

ATTEMPTS_PER_SECOND = 10_000_000_000

def strength_report(pwd: str):
    length = len(pwd)
    SYMBOLS = r"!@#$%^&*()_-+=[]{}|;:'\",.<>?/`~"
    classes = {
        "lower": bool(re.search(r"[a-z]", pwd)),
        "upper": bool(re.search(r"[A-Z]", pwd)),
        "digit": bool(re.search(r"\d",   pwd)),
        "symb" : bool(re.search(rf"[{re.escape(SYMBOLS)}]", pwd))
    }
    variety = sum(classes.values())

    pool = character_pool_size(classes)

    if pool == 0:
        return {
            "length": length,
            "variety": variety,
            "entropy_bits": 0,
            "label": entropy_label(0),
            "suggestions": ["Mot de passe invalide ou vide"],
            "time_to_crack": "immédiat"
        }

    bits = length * math.log2(pool)

    # Pénalités selon mauvaises pratiques
    penalties = 0
    suggestions = []

    if length < 8:
        penalties += 20
        suggestions.append("Augmenter la longueur")
    elif length < 12:
        suggestions.append("Augmenter la longueur pour plus de sécurité")

    if is_repeated_substring(pwd):
        penalties += 35
        suggestions.append("Éviter répétitions simples")

    if has_sequential_chars(pwd, seq_len=4):
        penalties += 30
        suggestions.append("Éviter séquences alphabétiques ou numériques")

    if re.fullmatch(r"(.)\1{3,}", pwd):
        penalties += 40
        suggestions.append("Éviter répétitions excessives d'un même caractère")

    if variety < 2:
        penalties += 25
        suggestions.append("Ajouter types de caractères manquants")

    effective_bits = max(bits - penalties, 0)

    label = entropy_label(effective_bits)
    if variety == 1:
        if effective_bits >= 60:
            label = "Moyenne"
        elif effective_bits >= 36:
            label = "Faible"
        else:
            label = "Très faible"
    elif variety == 2:
        if effective_bits >= 60:
            label = "Forte"
        elif effective_bits >= 36:
            label = "Moyenne"
        else:
            label = "Faible"

    combinations = 2 ** effective_bits
    avg_attempts = combinations / 2
    seconds_to_crack = avg_attempts / ATTEMPTS_PER_SECOND

    if not suggestions:
        suggestions.append("Aucune")

    return {
        "length": length,
        "variety": variety,
        "entropy_bits": round(effective_bits, 1),
        "label": label,
        "suggestions": suggestions,
        "time_to_crack": seconds_to_human(seconds_to_crack)
    }

def show_report(rep):
    label_w = 26
    def line(lbl,val): print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] {lbl.ljust(label_w)}: {WHITE}{val}{RESET}")

    print(f"{PURPLE_LIGHT}{BOLD}┌────────────── [Password Strength] ──────────────┐{RESET}")
    line("Longueur",             rep["length"])
    line("Types de caractères",  rep["variety"])
    line("Entropie estimée",     f'{rep["entropy_bits"]} bits')
    line("Robustesse",           rep["label"])
    line("Temps estimé crack",   rep["time_to_crack"])
    line("Suggestions",          ", ".join(rep["suggestions"]))
    print(f"{PURPLE_LIGHT}{BOLD}└──────────────────────────────────────────────────┘{RESET}")

def run():
    clear()
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}===== Password Strength Checker – tape 'q' pour quitter ====={RESET}\n")

    while True:
        pwd = input(f"{PURPLE_LIGHT}[Pwd Check]{RESET} Mot de passe : ")
        if pwd.lower() in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break
        if not pwd:
            print(f"{RED}Mot de passe vide.{RESET}\n")
            continue
        rep = strength_report(pwd)
        print()
        show_report(rep)
        print()

if __name__ == "__main__":
    run()
