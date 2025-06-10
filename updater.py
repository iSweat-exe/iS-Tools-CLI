import os, sys, io, zipfile, shutil, subprocess, tempfile, time
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    print("🛑  Le module 'requests' est requis.  pip install requests")
    sys.exit(1)

# —— Paramètres ——————————————————————————————————————————
LOCAL_VERSION = "1.1.0"                     # version actuelle
REPO          = "iSweat-exe/iS-Tools-CLI"  # owner/repo
BRANCH        = "main"
VERSION_FILE  = "Version.txt"               # fichier dans le repo
TIMEOUT       = 5                           # s
DEBUG         = False                        # active les logs debug

RAW_VERSION_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{VERSION_FILE}"
ZIP_URL         = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"

def debug(msg):
    if DEBUG:
        print(f"🐞 [DEBUG] {msg}")

def _version_tuple(v: str):
    debug(f"Conversion version '{v}' en tuple")
    return tuple(int(x) for x in v.strip("v").split("."))

def _get_headers():
    return {}

def _latest_version_online():
    url = RAW_VERSION_URL
    debug(f"Récupération version depuis : {url}")
    r = requests.get(url, headers=_get_headers(), timeout=TIMEOUT)
    r.raise_for_status()
    version_str = r.text.strip()
    debug(f"Version récupérée : {version_str}")
    return version_str

def _update_with_zip(tmp_dir):
    print("⬇️   Téléchargement de la dernière version...")
    debug(f"Téléchargement ZIP depuis : {ZIP_URL}")
    r = requests.get(ZIP_URL, headers=_get_headers(), timeout=TIMEOUT)
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

def check_and_update():
    print("🔍  Checking update...", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

    try:
        remote_version = _latest_version_online()
    except Exception as e:
        print(f"⚠️   Impossible de vérifier les mises à jour : {e}")
        debug(f"Exception levée lors de la requête de version : {e}")
        return

    debug(f"Comparaison versions : local={LOCAL_VERSION}, distant={remote_version}")
    if _version_tuple(remote_version) <= _version_tuple(LOCAL_VERSION):
        print(f"✅  Already up-to-date! (v{LOCAL_VERSION})")
        return

    print(f"🆕  Mise à jour disponible vers -> {remote_version}")
    c = input('Voulez-vous mettre à jour "iS-Tools" vers la version la plus récente ? [Y/n] ').strip().lower()
    if c not in ("", "y", "yes"):
        print("ℹ️  Mise à jour annulée.")
        return

    with tempfile.TemporaryDirectory() as tmp:
        debug(f"Répertoire temporaire créé : {tmp}")
        try:
            _update_with_zip(tmp)
            print("✅  Mise à jour installée. Relance iS‑Tool.")
            time.sleep(1)
            # Relance le script principal (main.py)
            script_path = Path(__file__).resolve().parent / "main.py"
            debug(f"Relance du script : {script_path}")
            subprocess.Popen([sys.executable, str(script_path)])
            sys.exit(0)
        except Exception as e:
            print(f"🛑  Mise à jour échouée : {e}")
            debug(f"Exception pendant _update_with_zip() : {e}")

if __name__ == "__main__":
    check_and_update()
