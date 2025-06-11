# coding: utf-8

# ─────────── Imports ───────────
import socket
import requests
import ipaddress
import json
import time
import shutil
import os

# ─────────── Couleurs ANSI 256 ───────────
PURPLE_VERY_LIGHT = '\033[38;5;201m'  # Lavande très clair
PURPLE_LIGHT = '\033[38;5;177m'       # Lavande clair
PURPLE_NORMAL = '\033[38;5;129m'      # Violet standard
PURPLE_DARK = '\033[38;5;90m'         # Violet foncé
PURPLE_VERY_DARK = '\033[38;5;54m'    # Lavande très foncé
WHITE = '\033[38;5;15m'
RED = '\033[38;5;196m'
BOLD = '\033[1m'
RESET = '\033[0m'

# ─────────── Countries ─────────
COUNTRY_NAMES = {
    "AF": "Afghanistan", "AL": "Albanie", "DZ": "Algérie", "AS": "Samoa américaines", "AD": "Andorre", "AO": "Angola",
    "AI": "Anguilla", "AQ": "Antarctique", "AG": "Antigua-et-Barbuda", "AR": "Argentine", "AM": "Arménie", "AW": "Aruba",
    "AU": "Australie", "AT": "Autriche", "AZ": "Azerbaïdjan", "BS": "Bahamas", "BH": "Bahreïn", "BD": "Bangladesh",
    "BB": "Barbade", "BY": "Biélorussie", "BE": "Belgique", "BZ": "Belize", "BJ": "Bénin", "BM": "Bermudes",
    "BT": "Bhoutan", "BO": "Bolivie", "BA": "Bosnie-Herzégovine", "BW": "Botswana", "BR": "Brésil", "BN": "Brunei",
    "BG": "Bulgarie", "BF": "Burkina Faso", "BI": "Burundi", "KH": "Cambodge", "CM": "Cameroun", "CA": "Canada",
    "CV": "Cap-Vert", "KY": "Îles Caïmans", "CF": "République centrafricaine", "TD": "Tchad", "CL": "Chili", "CN": "Chine",
    "CX": "Île Christmas", "CC": "Îles Cocos (Keeling)", "CO": "Colombie", "KM": "Comores", "CG": "République du Congo",
    "CD": "République démocratique du Congo", "CK": "Îles Cook", "CR": "Costa Rica", "CI": "Côte d'Ivoire", "HR": "Croatie",
    "CU": "Cuba", "CY": "Chypre", "CZ": "République tchèque", "DK": "Danemark", "DJ": "Djibouti", "DM": "Dominique",
    "DO": "République dominicaine", "EC": "Équateur", "EG": "Égypte", "SV": "El Salvador", "GQ": "Guinée équatoriale",
    "ER": "Érythrée", "EE": "Estonie", "SZ": "Eswatini", "ET": "Éthiopie", "FK": "Îles Malouines", "FO": "Îles Féroé",
    "FJ": "Fidji", "FI": "Finlande", "FR": "France", "GF": "Guyane française", "PF": "Polynésie française", "GA": "Gabon",
    "GM": "Gambie", "GE": "Géorgie", "DE": "Allemagne", "GH": "Ghana", "GI": "Gibraltar", "GR": "Grèce",
    "GL": "Groenland", "GD": "Grenade", "GP": "Guadeloupe", "GU": "Guam", "GT": "Guatemala", "GG": "Guernesey",
    "GN": "Guinée", "GW": "Guinée-Bissau", "GY": "Guyana", "HT": "Haïti", "HN": "Honduras", "HK": "Hong Kong",
    "HU": "Hongrie", "IS": "Islande", "IN": "Inde", "ID": "Indonésie", "IR": "Iran", "IQ": "Irak", "IE": "Irlande",
    "IM": "Île de Man", "IL": "Israël", "IT": "Italie", "JM": "Jamaïque", "JP": "Japon", "JE": "Jersey", "JO": "Jordanie",
    "KZ": "Kazakhstan", "KE": "Kenya", "KI": "Kiribati", "KP": "Corée du Nord", "KR": "Corée du Sud", "KW": "Koweït",
    "KG": "Kirghizistan", "LA": "Laos", "LV": "Lettonie", "LB": "Liban", "LS": "Lesotho", "LR": "Libéria", "LY": "Libye",
    "LI": "Liechtenstein", "LT": "Lituanie", "LU": "Luxembourg", "MO": "Macao", "MG": "Madagascar", "MW": "Malawi",
    "MY": "Malaisie", "MV": "Maldives", "ML": "Mali", "MT": "Malte", "MH": "Îles Marshall", "MQ": "Martinique",
    "MR": "Mauritanie", "MU": "Maurice", "YT": "Mayotte", "MX": "Mexique", "FM": "États fédérés de Micronésie", "MD": "Moldavie",
    "MC": "Monaco", "MN": "Mongolie", "ME": "Monténégro", "MS": "Montserrat", "MA": "Maroc", "MZ": "Mozambique",
    "MM": "Myanmar", "NA": "Namibie", "NR": "Nauru", "NP": "Népal", "NL": "Pays-Bas", "NC": "Nouvelle-Calédonie",
    "NZ": "Nouvelle-Zélande", "NI": "Nicaragua", "NE": "Niger", "NG": "Nigéria", "NU": "Niue", "NF": "Île Norfolk",
    "MK": "Macédoine du Nord", "MP": "Îles Mariannes du Nord", "NO": "Norvège", "OM": "Oman", "PK": "Pakistan",
    "PW": "Palaos", "PS": "Territoires palestiniens", "PA": "Panama", "PG": "Papouasie-Nouvelle-Guinée", "PY": "Paraguay",
    "PE": "Pérou", "PH": "Philippines", "PL": "Pologne", "PT": "Portugal", "PR": "Porto Rico", "QA": "Qatar",
    "RO": "Roumanie", "RU": "Russie", "RW": "Rwanda", "BL": "Saint-Barthélemy", "SH": "Sainte-Hélène",
    "KN": "Saint-Kitts-et-Nevis", "LC": "Sainte-Lucie", "MF": "Saint-Martin", "PM": "Saint-Pierre-et-Miquelon",
    "VC": "Saint-Vincent-et-les-Grenadines", "WS": "Samoa", "SM": "Saint-Marin", "ST": "Sao Tomé-et-Principe",
    "SA": "Arabie Saoudite", "SN": "Sénégal", "RS": "Serbie", "SC": "Seychelles", "SL": "Sierra Leone",
    "SG": "Singapour", "SK": "Slovaquie", "SI": "Slovénie", "SB": "Îles Salomon", "SO": "Somalie", "ZA": "Afrique du Sud",
    "SS": "Soudan du Sud", "ES": "Espagne", "LK": "Sri Lanka", "SD": "Soudan", "SR": "Suriname", "SE": "Suède",
    "CH": "Suisse", "SY": "Syrie", "TW": "Taïwan", "TJ": "Tadjikistan", "TZ": "Tanzanie", "TH": "Thaïlande",
    "TL": "Timor oriental", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga", "TT": "Trinité-et-Tobago", "TN": "Tunisie",
    "TR": "Turquie", "TM": "Turkménistan", "TC": "Îles Turks-et-Caïcos", "TV": "Tuvalu", "UG": "Ouganda",
    "UA": "Ukraine", "AE": "Émirats arabes unis", "GB": "Royaume-Uni", "US": "États-Unis", "UY": "Uruguay",
    "UZ": "Ouzbékistan", "VU": "Vanuatu", "VA": "Vatican", "VE": "Venezuela", "VN": "Viêt Nam", "WF": "Wallis-et-Futuna",
    "EH": "Sahara occidental", "YE": "Yémen", "ZM": "Zambie", "ZW": "Zimbabwe"
}

# ─────────── ASCII Art ─────────
ASCII_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                    ⠀
                         :**+ :::+*@@.                                                       
                 +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -                    
    @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:        
.#@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*      
#*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=       
      *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.      
      #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=          
     @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%@@@@@@@@@@@@@@@@@=  +        
    :@@@@@@@@@@@@@@:                   :@@    # - @@@@@@@ =@@@*#*@@@@@@@@@@@@@=.=-  #:       
     :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@             
      #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:            
        @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==            
        =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :           
            .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=              
               . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.         
                :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=            
               -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :     
                @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.  
                 @@@@@@@@@@@@@                #@@@@@@%@.                             :  :    
                  *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .@@@@=:@    
                   :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@   
                   :@@@@%@@                   .@@@@@-   .                     @@@@@@@@@@@@*  
                   :@@@@%@@                    *@@@-                          @@@@@@@@@@@@  
                   :@@@@%@@                                                        =@@@:    @=
                    =@@                                                              =    #+ 
                     @%                                                                        
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─── Impression centrée, ligne par ligne (animation) ─────────────────────────
def print_ascii_art():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    
    for line in ASCII_ART.strip('\n').splitlines():
        padding = max((terminal_width - len(line)) // 2, 0)
        print(' ' * padding + PURPLE_NORMAL + line + RESET)
        time.sleep(0.025)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def resolve_hostname(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print(f"{PURPLE_LIGHT}[Résolution DNS]{RESET} {hostname} → {ip}")
        return ip
    except socket.gaierror:
        print(f"{RED}[Erreur]{RESET} Impossible de résoudre le domaine : {hostname}")
        return None

def fetch_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            print(f"{RED}[Erreur]{RESET} Trop de requêtes. Veuillez attendre avant de réessayer.")
            return None
        elif response.status_code != 200:
            print(f"{RED}[Erreur]{RESET} Impossible de récupérer les informations (code {response.status_code}).")
            return None
        
        try:
            data = response.json()
            return data
        except json.JSONDecodeError:
            print(f"{RED}[Erreur]{RESET} Réponse JSON invalide.")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"{RED}[Erreur]{RESET} {e}")
        return None

def print_ip_info(data):
    fields = [
        ("IP", "ip"),
        ("HostName", "hostname"),
        ("City", "city"),
        ("Region", "region"),
        ("Country", "country"),
        ("Location", "loc"),
        ("Organisation", "org"),
        ("Postal", "postal"),
        ("Timezone", "timezone"),
        ("Anycast", "anycast")
    ]

    label_width = max(len(label) for label, _ in fields) + 2

    print(f"{PURPLE_LIGHT}{BOLD}┌────────────────── [IP LOOKUP] ──────────────────┐{RESET}")
    for label, key in fields:
        if key in data:
            value = data[key] if data[key] else "Non disponible"
            if label == "Country" and value != "Non disponible":
                country_code = value.upper()
                country_name = COUNTRY_NAMES.get(country_code, None)
                if country_name:
                    value = f"{country_name} ({country_code})"
                else:
                    value = country_code
            aligned_label = label.ljust(label_width)
            print(f"{PURPLE_LIGHT}├─ {WHITE}[{PURPLE_LIGHT}+{WHITE}]{PURPLE_LIGHT} {aligned_label}: {WHITE}{value}{RESET}")
    print(f"{PURPLE_LIGHT}{BOLD}└─────────────────────────────────────────────────┘{RESET}")

# ─────────── Programme principal ─────────
def run():
    clear_screen()
    os.system("title iS-Tools - IP Lookup") 
    print_ascii_art()

    print()
    print(f"{PURPLE_LIGHT}===== IP Lookup - Tapez 'q' ou 'quit' pour quitter ====={RESET}")
    while True:
        target = input(f"{PURPLE_LIGHT}[IP Lookup] -{RESET} Entrez l'adresse IP ou l'URL cible : ").strip()
        print()
        if target.lower() in ('q', 'quit'):
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            print()
            break

        ip = target
        if not is_valid_ip(target):
            ip = resolve_hostname(target)
            if ip is None:
                continue

        data = fetch_ip_info(ip)
        if data is None:
            continue

        print_ip_info(data)
        print()

if __name__ == "__main__":
    run()
