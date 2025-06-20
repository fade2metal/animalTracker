from subprocess import run
from sys import exit
from pathlib import Path
from os import system
import logging

REPO_URL = "https://github.com/fade2metal/"
APP_DIR = Path("animalTracker")
ENTRY_SCRIPT = APP_DIR / "main.py"
USERNAME = "fade2metal"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# set git user
run(["git", "config", "--global", "user.name", USERNAME], check=True)

def clone_or_update_repo():
    '''
    function for cloning or updating repo
    '''
    if APP_DIR.exists() and (APP_DIR / ".git").exists():
        logger.info("Updating repo...")
        run(["git", "-C", str(APP_DIR), "pull"], check=True)
    else:
        logger.info("Cloning repo...")
        run(["git", "clone", REPO_URL + str(APP_DIR) + ".git"], check=True)

def start_app():
    '''
    function for starting the app
    '''
    if not ENTRY_SCRIPT.exists():
        logger.error(f"Fehler: {ENTRY_SCRIPT} existiert nicht")
        exit(1)
    
    logger.info(f"Starte App: {ENTRY_SCRIPT}")
    run(["python3", str(ENTRY_SCRIPT)], check=True, capture_output=True)

if __name__ == "__main__":
    clone_or_update_repo()
    start_app()