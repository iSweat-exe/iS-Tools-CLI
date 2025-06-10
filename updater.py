"""
updater.py – gère les mises à jour automatiques d’iS‑Tool via GitHub
© 2025 iSweat‑exe
"""

import os, sys, io, zipfile, shutil, subprocess, tempfile, time
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    print("🛑  Le module 'requests' est requis.  pip install requests")
    sys.exit(1)

# —— Paramètres ——————————————————————————————————————————
LOCAL_VERSION = "1.0.0"                     # version actuelle
REPO          = "iSweat-exe/iS-Tools-CLI"   # owner/repo
BRANCH        = "main"
VERSION_FILE  = "Version.txt"               # fichier dans le repo
TIMEOUT       = 5                           # s
DEBUG         = True                        # active les logs debug

RAW_VERSION_URL_PUBLIC = (
    f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{VERSION_FILE}"
)
ZIP_URL = (
    f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"
)

GITHUB_API_REPO_URL = f"https://api.github.com/repos/{REPO}"

def debug(msg):
    """Affiche un message de debug si activé"""
    if DEBUG:
        print(f"🐞 [DEBUG] {msg}")

def _version_tuple(v: str):
    debug(f"Conversion version '{v}' en tuple")
    return tuple(int(x) for x in v.strip("v").split("."))

def _is_repo_private(token=None):
    """
    Interroge l'API GitHub pour savoir si le repo est privé.
    Si token est donné, l'utilise dans les headers pour auth.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    debug(f"Vérification si repo est privé via API : {GITHUB_API_REPO_URL}")
    try:
        r = requests.get(GITHUB_API_REPO_URL, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        private = data.get("private", False)
        debug(f"Réponse API : private={private}")
        return private
    except Exception as e:
        debug(f"Erreur lors de la vérification du repo privé : {e}")
        # En cas d'erreur, on suppose public (pour éviter blocage)
        return False

def _latest_version_online():
    """
    Tente d'utiliser le token si repo privé, sinon requête publique.
    Le token est lu dans la variable d'environnement GITHUB_TOKEN.
    """
    token = os.getenv("GITHUB_TOKEN")

    if _is_repo_private(token):
        debug("Repo privé détecté, utilisation du token pour la requête")
        if not token:
            raise RuntimeError("Le dépôt est privé, mais la variable GITHUB_TOKEN n'est pas définie.")
        headers = {"Authorization": f"token {token}"}
        url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{VERSION_FILE}"
        debug(f"Requête avec token vers : {url}")
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        debug(f"Version trouvée sur le repo (privé) : {r.text.strip()}")
        return r.text.strip()
    else:
        debug("Repo public détecté, requête publique")
        debug(f"Requête vers : {RAW_VERSION_URL_PUBLIC}")
        r = requests.get(RAW_VERSION_URL_PUBLIC, timeout=TIMEOUT)
        r.raise_for_status()
        debug(f"Version trouvée sur le repo (public) : {r.text.strip()}")
        return r.text.strip()

def _update_with_git():
    print("🔄  Mise à jour via git pull...")
    debug("Commande : git pull origin " + BRANCH)
    res = subprocess.call(["git", "pull", "origin", BRANCH])
    if res == 0:
        print("✅  Mise à jour terminée ! Relance iS‑Tool.")
        sys.exit(0)
    print("⚠️   git pull a échoué, bascule sur la méthode ZIP...")
    debug(f"git pull return code: {res}")

def _update_with_zip(tmp_dir):
    print("⬇️   Téléchargement de la dernière version...")
    debug(f"Téléchargement ZIP depuis : {ZIP_URL}")
    r = requests.get(ZIP_URL, timeout=TIMEOUT)
    r.raise_for_status()

    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(tmp_dir)
    debug(f"Archive extraite dans : {tmp_dir}")

    extracted_root = next(Path(tmp_dir).iterdir())
    target_dir = Path(__file__).resolve().parent
    debug(f"Répertoire cible : {target_dir}")
    debug(f"Contenu extrait : {list(extracted_root.iterdir())}")

    print("📁  Copie des nouveaux fichiers...")
    for item in extracted_root.iterdir():
        dest = target_dir / item.name
        debug(f"Copie {item} → {dest}")
        if dest.exists():
            if dest.is_file():
                dest.unlink()
                debug(f"Fichier supprimé : {dest}")
            else:
                shutil.rmtree(dest)
                debug(f"Dossier supprimé : {dest}")
        shutil.move(str(item), dest)
        debug(f"Déplacé : {item} → {dest}")

def check_and_update(auto: bool = True):
    print("🔍  Checking update...", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

    try:
        remote = _latest_version_online()
    except Exception as e:
        print(f"⚠️   Impossible de vérifier les mises à jour : {e}")
        debug(f"Exception levée lors de la requête de version : {e}")
        return

    debug(f"Comparaison versions : local={LOCAL_VERSION}, distant={remote}")
    if _version_tuple(remote) <= _version_tuple(LOCAL_VERSION):
        print(f"✅  Vous êtes à jour ! (v{LOCAL_VERSION})")
        return

    print(f"🆕  Nouvelle version trouvée : {remote}  (actuelle {LOCAL_VERSION})")
    if not auto:
        c = input("Mettre à jour maintenant ? [o/N] ").lower()
        if c != "o":
            print("ℹ️  Mise à jour annulée.")
            return

    if (Path(__file__).resolve().parent / ".git").exists():
        debug("Répertoire .git détecté, tentative git pull")
        _update_with_git()
    else:
        debug("Pas de .git → fallback ZIP")

    with tempfile.TemporaryDirectory() as tmp:
        debug(f"Répertoire temporaire créé : {tmp}")
        try:
            _update_with_zip(tmp)
            print("✅  Mise à jour installée. Relance iS‑Tool.")
            time.sleep(1)
            sys.exit(0)
        except Exception as e:
            print(f"🛑  Mise à jour échouée : {e}")
            debug(f"Exception pendant _update_with_zip() : {e}")
