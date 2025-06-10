#!/usr/bin/env python3
# coding: utf-8
"""
Discord User Lookup – iS‑Tools (sans token)
Dépendances : requests  (pip install requests)
"""

import os, shutil, time, datetime, requests, json

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
RED           = '\033[38;5;196m'
BOLD          = '\033[1m'
RESET         = '\033[0m'

# ─────────── ASCII Art (same look) ───────
ASCII_ART = r"""
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                   
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                 
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                 
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                  
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                     
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@                         
"""

# ─────────── Badge flags → label ─────────
BADGE_FLAGS = {
    1 << 0 : "Discord Staff",
    1 << 1 : "Partner",
    1 << 2 : "HypeSquad Events",
    1 << 3 : "Bug Hunter Lv1",
    1 << 6 : "House Bravery",
    1 << 7 : "House Brilliance",
    1 << 8 : "House Balance",
    1 << 9 : "Early Supporter",
    1 << 14: "Bug Hunter Lv2",
    1 << 16: "Verified Bot",
    1 << 17: "Early Verified Dev",
    1 << 18: "Moderator",
    1 << 19: "Bot HTTP Interactions",
    1 << 22: "Active Developer",
    1 << 23: "Spammer"
}

# ─────────── Utils ───────────────────────
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    width = shutil.get_terminal_size((80, 20)).columns
    for line in ASCII_ART.strip("\n").splitlines():
        pad = max((width - len(line)) // 2, 0)
        print(' ' * pad + PURPLE_NORMAL + line + RESET)
        time.sleep(0.025)

def snowflake_to_date(sf: int) -> str:
    epoch = 1420070400000
    ts_ms = (sf >> 22) + epoch
    return datetime.datetime.utcfromtimestamp(ts_ms/1000)\
           .strftime("%d %b %Y %H:%M:%S UTC")

def cdn_url(user_id: str, hash_, route: str):
    if not hash_: return "—"
    ext = "gif" if hash_.startswith("a_") else "png"
    return f"https://cdn.discordapp.com/{route}/{user_id}/{hash_}.{ext}?size=1024"

def badges_from_flags(flags: int):
    return [label for bit, label in BADGE_FLAGS.items() if flags & bit]

def print_raw_json(data):
    print(f"{PURPLE_LIGHT}[JSON brut reçu]{RESET}")
    print(json.dumps({"data": data}, indent=4, ensure_ascii=False))


# ─────────── API call (public) ───────────
API = "https://japi.rest/discord/v1/user/{}"

def fetch_user(uid: str):
    r = requests.get(API.format(uid), timeout=7)
    if r.status_code == 429:
        raise RuntimeError("Rate‑limit atteint ; réessaie plus tard ou avec proxy.")
    if r.status_code == 404:
        raise RuntimeError("Utilisateur introuvable.")
    if r.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {r.status_code}")
    return r.json()["data"]          # structure { "data": { ... } }

# ─────────── Affichage ───────────────────
def print_user(d):
    label_w = 30
    def line(lbl, val):
        print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] {lbl.ljust(label_w)}: {WHITE}{val}{RESET}")

    flags     = d.get("public_flags", 0)
    flags_arr = d.get("public_flags_array", [])

    # Combine les badges, retire les doublons même s'ils ont des écritures différentes
    raw_badges = badges_from_flags(flags) + flags_arr

    unique_badges = {}
    for badge in raw_badges:
        # clé = seulement lettres/chiffres en minuscules
        key = "".join(ch for ch in badge.lower() if ch.isalnum())
        if key not in unique_badges:
            unique_badges[key] = badge   # on garde la 1ʳᵉ version lisible

    badge_list = sorted(unique_badges.values())

    print(f"{PURPLE_LIGHT}{BOLD}┌───────────────────────────── [Discord User Lookup] ──────────────────────────────┐{RESET}")
    line("Global Name",        d.get("global_name", "—"))
    line("Username",           f'{d["username"]}#{d.get("discriminator","0")}')
    line("Avatar URL",         d.get("avatarURL",  cdn_url(d["id"], d.get("avatar"), "avatars")))
    line("Banner URL",         d.get("bannerURL",  cdn_url(d["id"], d.get("banner"), "banners")))
    line("Date de création",   snowflake_to_date(int(d["id"])))
    line("Bot",                "Yes" if d.get("bot") else "No")
    line("Spammer Flag",       "Yes" if flags & (1 << 23)            else "No")
    line("Provisional Account","Yes" if flags & (1 << 21)            else "No")
    line("Banner Color",       d.get("banner_color", "—"))
    accent = d.get("accent_color")
    line("Accent Color",       f'#{accent:06x}' if accent else "—")

    deco = d.get("avatar_decoration_data") or {}
    line("Avatar Deco SKU ID", deco.get("sku_id", "—"))

    clan = d.get("clan") or d.get("primary_guild") or {}
    line("Clan Tag",           clan.get("tag", "—"))
    line("Clan Guild ID",      clan.get("identity_guild_id", "—"))

    line("Badges",             ", ".join(badge_list) if badge_list else "Aucun")
    print(f"{PURPLE_LIGHT}{BOLD}└──────────────────────────────────────────────────────────────────────────────────┘{RESET}")

# ─────────── Programme principal ─────────
def run():
    clear()
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}===== Discord User Lookup – tape 'q' pour quitter ====={RESET}\n")

    while True:
        uid = input(f"{PURPLE_LIGHT}[User Lookup]{RESET} ID Discord : ").strip()
        if uid.lower() in ("q", "quit"):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            print()
            break
        if not uid.isdigit() or len(uid) < 17:
            print(f"{RED}ID non valide.{RESET}\n"); continue
        try:
            data = fetch_user(uid)
            print()
            print_user(data)
            print()
        except Exception as e:
            print(f"{RED}[Erreur]{RESET} {e}\n")

if __name__ == "__main__":
    run()
