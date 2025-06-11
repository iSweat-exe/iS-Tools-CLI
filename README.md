<h1 align="center">
  🚀 iS-Tools CLI ( Work In Progress )
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" />
  <img src="https://img.shields.io/badge/status-WIP-orange.svg" />
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" />
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg" />
</p>

---

<h2 align="center">📦 Présentation</h2>

**iS-Tools CLI** est un CLI tool conçu pour les passionnés de cybersécurité, les pentesters et curieux de l’OSINT. Il regroupe plusieurs modules utiles, souvent niche, issus de mes propres idées, pensées et expérimentations.

> 🛠️ Ce projet est développé **entièrement sur mon temps libre**.  
> Il évolue selon mon inspiration, avec des outils qui peuvent aller du scan IP, jusqu’au piratage de caméras vulnérables.
> Le but est de **centraliser plein de petits outils utiles, originaux et efficaces** dans une interface CLI agréable.

---

>[!NOTE]
> **Statut : En cours de développement (Work In Progress)**  
> Le projet évolue fréquemment. Il peut contenir des fonctionnalités expérimentales ou instables.

>[!WARNING]
> **Utilisation encadrée uniquement**  
> iS-Tools CLI est destiné à un usage **éducatif** ou dans le cadre de **tests d’intrusion autorisés**.  
> Toute utilisation non encadrée ou illégale est strictement interdite et **relève uniquement de la responsabilité de l’utilisateur**.  
> L’auteur (**iSweat**) ne pourra en aucun cas être tenu responsable d’un usage abusif ou détourné.

---

<h2 align="center">⚙️ Modules actuellement disponibles</h2>

- ✅ IP Lookup  
- ✅ IP Pinger  
- ✅ IP Scanner  
- ✅ Website Scanner  
- ✅ SQL Injection (bientôt remplacé par sqlmap)  
- ✅ DVR Credentials Exploit  
- ✅ Crypto Wallets Checker  
- ✅ Password Generator  
- ✅ Password Encrypted  
  (BCRYPT, MD5, SHA-1, SHA-256, PBKDF2, Base64 Encode)  
- ✅ Password Decrypted  
- ✅ Password Checker  
- ✅ Dox Creator  
- ✅ EXIF Reader  
- ✅ Discord User Info  
- ✅ Discord Token  
- ✅ Discord Invite Info  

> 🔜 À venir : sqlmap, bruteforce SSH (port 22), bruteforce FTP (port 21), XSStrike  
> *Certains modules listés pourraient ne jamais voir le jour. (À venir)*


---

<h2 align="center">🧰 Informations techniques</h2>

- 📁 Langage : Python 3.8+
- 💻 Compatibilité : Windows / Linux
- 🎨 Interface CLI colorée en ANSI 256 avec `colorama`, `rich`, etc.  

---

<h2 align="center">🖥️ Utilisation</h2>

##### Téléchargement et installation :
```bash
git clone https://github.com/tonpseudo/is-tools-cli.git
cd is-tools-cli
python3 main.py
```

##### Pour afficher l'aide :
```bash
python main.py --help
```

##### Pour lancer la mise à jour :
```bash
python main.py --update
```

Entrez le numéro du module pour naviguer dans le menu.

---

<h2 align="center">💡 Suggestions bienvenues</h2>

Tu veux proposer une idée de module ?  
Tu as trouvé un bug ou une amélioration possible ?  
👉 **N'hésite pas à ouvrir une issue ou me contacter sur Discord** *(isweatmc)*.

---

<h2 align="center">🎯 Objectif</h2>

Créer un outil tout-en-un, unique, original, utile, souvent niche mais toujours fonctionnel.  
Une boîte à outils pour tester, apprendre et s’amuser.

---

<h2 align="center">📬 Contact</h2>

- 👤 Auteur : **iSweat**
- 💬 Discord : `isweatmc`

---

<h2 align="center">✅ Version actuelle</h2>

| Version | Date       | Changements principaux                                          |
|---------|------------|----------------------------------------------------------------|
| v1.2.0   | XX/XX/XXXX |🛠️ Intégration de sqlmap<br>🔑 Bruteforce SSH (port 22)<br>🔑 Bruteforce FTP (port 21)<br>🔗 XSStrike |
| v1.1.0  | 11/06/2025 | ✨ Système de mise à jour ajouté<br>🙌 Crédits ajoutés<br>📂 Dox Creator<br>🖼️ EXIF Reader<br>👤 Discord User Info<br>🔑 Discord Token<br>🔗 Discord Invite Info<br>✅ Password Checker<br>🔐 Password Generator<br>🚀 Repository public GitHub<br>📜 Licence MIT<br>📝 `README.md` ajouté |
| v1.0.0  | 07/06/2025 | 🚀 Release initiale avec les 6 modules principaux fonctionnels |

---
