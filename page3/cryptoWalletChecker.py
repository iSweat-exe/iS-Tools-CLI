# ─────────── Imports ───────────
import re

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_LIGHT = '\033[38;5;177m'
WHITE = '\033[38;5;15m'
GREEN = '\033[38;5;46m'
RED = '\033[38;5;196m'
RESET = '\033[0m'

# ─────────── ASCII Art ─────────

# ─────────── Bitcoin Validation ─────────
def is_valid_btc(address):
    # Bitcoin Legacy (1, 3) et Bech32 (bc1)
    if re.match(r'^(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return True
    if re.match(r'^(bc1)[a-z0-9]{39,59}$', address):
        return True
    return False

# ─────────── Ethereum Validation ─────────
def is_valid_eth(address):
    # Ethereum : commence par 0x + 40 hex chars
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return True
    return False

# ─────────── Monero Validation ─────────
def is_valid_xmr(address):
    # Monero : 95 ou 106 caractères, commence par 4
    if re.match(r'^(4)[0-9A-Za-z]{93,106}$', address):
        return True
    return False

# ─────────── Litecoin Validation ─────────
def is_valid_ltc(address):
    # Litecoin Legacy (L,M) et Bech32 (ltc1)
    if re.match(r'^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$', address):
        return True
    if re.match(r'^(ltc1)[a-z0-9]{39,59}$', address):
        return True
    return False

# ─────────── Check Wallet ─────────
def check_wallet(address):
    if is_valid_btc(address):
        return "Bitcoin", True
    elif is_valid_eth(address):
        return "Ethereum", True
    elif is_valid_ltc(address):
        return "Litecoin", True
    elif is_valid_xmr(address):
        return "Monero", True
    else:
        return None, False

# ─────────── Programme principal ─────────
def run():
    print(f"{PURPLE_LIGHT}===== Crypto Wallet Checker - Tapez 'q' ou 'quit' pour quitter ====={RESET}")
    while True:
        addr = input(f"{PURPLE_LIGHT}[CryptoWalletChecker] -{RESET} Entrez une adresse de portefeuille crypto : ").strip()
        if addr.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[CryptoWalletChecker] -{RESET} Fermeture de l'outil.")
            break
        crypto, valid = check_wallet(addr)
        if valid:
            print(f"{GREEN}[Valid]{RESET} Adresse {crypto} valide : {WHITE}{addr}{RESET}\n")
        else:
            print(f"{RED}[Invalid]{RESET} Adresse crypto invalide : {WHITE}{addr}{RESET}\n")

if __name__ == "__main__":
    run()
