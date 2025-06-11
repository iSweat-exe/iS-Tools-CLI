# coding: utf-8

# ─────────── Imports ───────────
import os, shutil, time, json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_LIGHT  = '\033[38;5;177m'
PURPLE_NORMAL = '\033[38;5;129m'
WHITE         = '\033[38;5;15m'
GREEN         = '\033[38;5;46m'
RED           = '\033[38;5;196m'
CYAN_LINK     = '\033[38;5;87m'
BOLD          = '\033[1m'
RESET         = '\033[0m'

# ─────────── ASCII Art ─────────
ASCII_ART = r"""                                                                                                
                                          ...:----:...                                              
                                     .:=#@@@@@@@@@@@@@@%*-..                                        
                                  .:#@@@@@@@%#*****#%@@@@@@@+..                                     
                               ..-@@@@@%-...... ........+@@@@@@..                                   
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.                                  
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.                                
                            .#@@@%.                 .=@@@@@=. .@@@@-.                               
                           .=@@@#.                    .:%@@@*. -@@@%:.                              
                           .%@@@-                       .*@@*. .+@@@=.                              
                           :@@@#.                              .-@@@#.                              
                           -@@@#                                :%@@@.                              
                           :@@@#.                              .-@@@#.                              
                           .%@@@-.                             .+@@@=.                              
                           .+@@@#.                             -@@@%:.                              
                            .*@@@%.                          .:@@@@-.                               
                             .+@@@@=..                     ..*@@@@:.                                
                               :%@@@@-..                ...+@@@@*.                                  
                               ..-@@@@@%=...         ...*@@@@@@@@#.                                 
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.                              
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.                            
                                        .....:::::::....       ...+@@@@%:                           
                                                                  ..+@@@@%-.                        
                                                                    ..=@@@@%-.                      
                                                                      ..=@@@@@=.                    
                                                                         .=%@@@@=.                  
                                                                          ..-%@@@-.                 
                                                                             ....
                          
"""

# ─────────── Utils écriture CLI ─────────
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    width = shutil.get_terminal_size((80, 20)).columns
    for l in ASCII_ART.strip("\n").splitlines():
        pad = max((width - len(l)) // 2 - 10, 0)
        print(' ' * pad + PURPLE_NORMAL + l + RESET)
        time.sleep(0.025)

def line(label, value, label_w=15):
    print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}] "
          f"{label.ljust(label_w)} : {WHITE}{value}{RESET}")

def convert_gps(coord, ref):
    try:
        d, m, s = map(float, coord)
        val = d + m / 60 + s / 3600
        return -val if ref in ('S', 'W') else val
    except Exception as e:
        print(f"{RED}[EXIF Error] - Conversion GPS : {e}{RESET}")
        return None

def clean_filename(name):
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)

def format_exif_date(s):
    try:
        return datetime.strptime(s, "%Y:%m:%d %H:%M:%S")\
                       .strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return s

# ─────────── Extraction EXIF ────────────
def extract_exif(img_path):
    try:
        img = Image.open(img_path)
        raw  = img._getexif()
        if not raw:
            print(f"{PURPLE_LIGHT}[EXIF Reader]{RESET} - Aucune donnée EXIF.{RESET}")
            return None
        exif, gps = {}, {}
        for tag_id, val in raw.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                for gid, gval in val.items():
                    gps[GPSTAGS.get(gid, gid)] = gval
                exif["GPSInfo"] = gps
            else:
                exif[tag] = val
        return exif
    except Exception as e:
        print(f"{RED}[EXIF Error] - Extraction : {e}{RESET}")
        return None

# ─────────── Affichage formaté ──────────
def display_exif(exif):
    # — Appareil —
    make  = exif.get("Make", "").strip()
    model = exif.get("Model", "").strip()
    print(f"{PURPLE_LIGHT}┌────────────── [Appareil Photo] ───────────────┐{RESET}")
    line("", f"{make} {model}" if (make or model) else "—", label_w=0)
    print(f"{PURPLE_LIGHT}└───────────────────────────────────────────────┘{RESET}")

    # — GPS —
    gps = exif.get("GPSInfo", {})
    print(f"{PURPLE_LIGHT}┌────────────────────────────────────────── [Coordonnées GPS] ───────────────────────────────────────────┐{RESET}")
    lat, lat_ref = gps.get("GPSLatitude"), gps.get("GPSLatitudeRef")
    lon, lon_ref = gps.get("GPSLongitude"), gps.get("GPSLongitudeRef")
    if lat and lon and lat_ref and lon_ref:
        lat_dec, lon_dec = convert_gps(lat, lat_ref), convert_gps(lon, lon_ref)
        if lat_dec is not None and lon_dec is not None:
            line("Latitude",  f"{lat_dec:.6f}",   label_w=12)
            line("Longitude", f"{lon_dec:.6f}",   label_w=12)
            maps = f"https://maps.google.com/?q={lat_dec},{lon_dec}"
            line("Google Maps (CTRL + Click)", CYAN_LINK + maps + RESET, 30)
        else:
            line("", "Coordonnées GPS invalides", 0)
    else:
        line("", "Coordonnées GPS absentes", 0)
    print(f"{PURPLE_LIGHT}└────────────────────────────────────────────────────────────────────────────────────────────────────────┘{RESET}")

    # — Tags principaux —
    print(f"{PURPLE_LIGHT}┌─────────────── [Données EXIF] ────────────────┐{RESET}")
    main = ["DateTimeOriginal","DateTime","FocalLength",
            "ISOSpeedRatings","ExposureTime","FNumber"]
    for tag in main:
        if tag in exif:
            val = exif[tag]
            if tag in ("DateTimeOriginal","DateTime"):
                val = format_exif_date(str(val))
            elif isinstance(val, tuple) and len(val)==2:
                val = f"{val[0]/val[1]:.3f}"
            line(tag, val, 16)
    print(f"{PURPLE_LIGHT}└───────────────────────────────────────────────┘{RESET}")

    # — Autres —
    others = {k:v for k,v in exif.items()
              if k not in main+["Make","Model","GPSInfo"]}
    if others:
        print(f"{PURPLE_LIGHT}┌─────────────── [Autres Métadonnées] ────────────────┐{RESET}")
        for k,v in sorted(others.items()):
            if isinstance(v, tuple) and len(v)==2:
                v = f"{v[0]/v[1]:.3f}"
            line(k, v, 22)
        print(f"{PURPLE_LIGHT}└─────────────────────────────────────────────────────┘{RESET}")

# ─────────── Sauvegardes TXT / JSON ─────
def save_txt(exif, img):
    fname = clean_filename(os.path.basename(img)) + "_exif.txt"
    try:
        with open(fname, "w", encoding="utf-8") as f:
            for k,v in exif.items():
                f.write(f"{k}: {v}\n")
        print(f"{PURPLE_LIGHT}[EXIF Saver] - {WHITE}TXT sauvegardé : {GREEN}{fname}{RESET}")
    except Exception as e:
        print(f"{RED}[EXIF Error] - Save TXT : {e}{RESET}")

def save_json(exif, img):
    fname = clean_filename(os.path.basename(img)) + "_exif.json"

    def conv(val):
        if isinstance(val, (list, tuple)):
            return [conv(x) for x in val]
        if isinstance(val, dict):
            return {k: conv(v) for k, v in val.items()}
        try:
            return float(val)
        except (TypeError, ValueError):
            return str(val)

    try:
        with open(fname, "w", encoding="utf-8") as f:
            json.dump({k: conv(v) for k, v in exif.items()},
                      f, indent=4, ensure_ascii=False)
        print(f"{PURPLE_LIGHT}[EXIF Saver] - {WHITE}JSON sauvegardé : {GREEN}{fname}{RESET}")
    except Exception as e:
        print(f"{RED}[EXIF Error] - Save JSON : {e}{RESET}")

# ─────────── Programme principal ─────────
def run():
    clear()
    os.system("title iS‑Tools – EXIF Reader" if os.name=="nt" else "")
    print_ascii_art()
    print()
    print(f"{PURPLE_LIGHT}{BOLD}===== EXIF Reader - Analyse des métadonnées ====={RESET}\n")

    img = input(f"{PURPLE_LIGHT}[EXIF Reader]{RESET} - Entrez le chemin de l'image : ").strip()
    if not os.path.isfile(img):
        print(f"{RED}[EXIF Error] - Fichier introuvable.{RESET}")
        return

    exif = extract_exif(img)
    if not exif: return

    print(f"{PURPLE_LIGHT}[EXIF Scanner]{RESET} - Données EXIF détectées !\n")
    display_exif(exif)

    if input(f"\n{PURPLE_LIGHT}[EXIF Saver]{RESET} - Sauvegarder dans un fichier texte ? (y/n) : ").lower()=="y":
        save_txt(exif, img)
    if input(f"{PURPLE_LIGHT}[EXIF Saver]{RESET} - Sauvegarder au format JSON ? (y/n) : ").lower()=="y":
        save_json(exif, img)

if __name__ == "__main__":
    run()
