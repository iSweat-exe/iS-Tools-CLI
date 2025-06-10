import os
import shutil
import time
import re
from colorama import init, Fore, Style

init(autoreset=True)

# Couleurs
DISCORD_BLUE = '\033[38;5;33m'
PASTEL_PINK = '\033[38;5;213m'
PASTEL_PURPLE = '\033[38;5;177m'
PURPLE_VERY_LIGHT = '\033[38;5;201m'
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
PURPLE_DARK = '\033[38;5;90m'
PURPLE_VERY_DARK = '\033[38;5;54m'
RED = '\033[38;5;196m'
BLUE = '\033[38;5;21m'
WHITE = '\033[38;5;15m'
RESET = '\033[0m'
BOLD = '\033[1m'

LINE_DELAY = 0.025

def center_text(text):
    width = shutil.get_terminal_size((80, 20)).columns
    lines = text.splitlines()
    return "\n".join(line.center(width) for line in lines)

ANSI_ESCAPE = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]')
def print_with_loading(text, delay=0.01, color=''):
    width = shutil.get_terminal_size((80, 20)).columns
    lines = text.splitlines()
    for line in lines:
        if line.strip() == '':
            print()
        else:
            # Enlève les codes ANSI pour le calcul du centrage
            clean_line = ANSI_ESCAPE.sub('', line)
            padding = (width - len(clean_line)) // 2
            # Reconstruit la ligne colorée avec le bon padding
            print(' ' * padding + f"{color}{line}{RESET}", flush=True)
        time.sleep(delay)

# Banner ASCII art
banner_art = f"""
                              {BLUE} ██▓  ██████{WHITE}     ▄▄▄█████▓ ▒█████   ▒█████ {RED} ██▓      ██████ {RESET}
                              {BLUE}▓██▒▒██    ▒{WHITE}    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒{RED}▓██▒    ▒██    ▒ {RESET}
                              {BLUE}▒██▒░ ▓██▄  {WHITE}    ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒{RED}▒██░    ░ ▓██▄   {RESET}
                              {BLUE}░██░  ▒   ██▒{WHITE}   ░ ▓██▓ ░ ▒██   ██░▒██   ██░{RED}▒██░      ▒   ██▒{RESET}
                              {BLUE}░██░▒██████▒▒{WHITE}     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░{RED}░██████▒▒██████▒▒{RESET}
                              {BLUE}░▓  ▒ ▒▓▒ ▒ ░{WHITE}     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ {RED}░ ▒░▓  ░▒ ▒▓▒ ▒ ░{RESET}
                              {BLUE} ▒ ░░ ░▒  ░ ░{WHITE}       ░      ░ ▒ ▒░   ░ ▒ ▒░ {RED}░ ░ ▒  ░░ ░▒  ░ ░{RESET}
                              {BLUE} ▒ ░░  ░  ░{WHITE}       ░      ░ ░ ░ ▒  ░ ░ ░ ▒  {RED}  ░ ░   ░  ░  ░  {RESET}
                              {BLUE} ░        ░{WHITE}                  ░ ░      ░ ░  {RED}    ░  ░      ░  {RESET}
"""

# Banner ASCII art
# banner_art = r"""
#  ██▓  ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
# ▓██▒▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
# ▒██▒░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
# ░██░  ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
# ░██░▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
# ░▓  ▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
#  ▒ ░░ ░▒  ░ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
#  ▒ ░░  ░  ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
#  ░        ░                  ░ ░      ░ ░      ░  ░      ░  
# """

credits_lines = [
    f"                                                                                ",
    f"                             {WHITE}Thanks you for using iS-Tools{WHITE}        ",
    f"                                                                                ",
    f"                                      {WHITE}Contact                            ",
    f"                        {WHITE}[https://github.com/isweat-exe/iSTools]{WHITE}   ",
    f"                                    {BLUE}Discord{WHITE}  : isweatmc{WHITE}     ",
    f"                                                                                ",
    f"                                   {WHITE}Version  : 1.0.0{WHITE}               ",
    f"                              {WHITE}Last Update  : 08/06/2025{WHITE}           ",
    f"                                                                                ",
    f"                                {WHITE}I’m root, deal with it.{WHITE}           ",
    f"                                     {WHITE}08/06/2025                          ",
    f"                                        {BLUE}iS{WHITE}we{RED}at{RESET}         "
]

def run():
    os.system("title iS-Tools - Info Software")
    os.system('cls' if os.name == 'nt' else 'clear')
    print_with_loading(banner_art, delay=LINE_DELAY, color=PURPLE_VERY_LIGHT + BOLD)
    print()
    print_with_loading("\n".join(credits_lines), delay=LINE_DELAY, color=PASTEL_PURPLE + BOLD)
    print()
    input(f"\n{PASTEL_PURPLE}[iS-Tool Info] -{RESET} {WHITE}Appuie sur Entrée pour revenir au menu...{RESET}")

if __name__ == "__main__":
    run()
