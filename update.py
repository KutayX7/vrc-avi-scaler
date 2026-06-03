import subprocess
import os

def _discard_unstaged():
    print("[INFO] Discarding unstaged changes...")
    returncode = subprocess.run(["git", "checkout", "."]).returncode
    if returncode == 0:
        print("[INFO] Discarded unstaged changes.")
    else:
        print("[ERROR] Failed to discard unstaged changes. Return code:", returncode)
    return returncode

def _discard_staged():
    print("[INFO] Discarding staged changes...")
    returncode = subprocess.run(["git", "reset", "--hard", "HEAD"]).returncode
    if returncode == 0:
        print("[INFO] Discarded staged changes.")
    else:
        print("[ERROR] Failed to discard staged changes. Return code:", returncode)
    return returncode

def _discard_current():
    return _discard_unstaged() or _discard_staged() or 0

def _fetch():
    print("[INFO] Fetching...")
    returncode = subprocess.run(["git", "fetch"]).returncode
    if returncode == 0:
        print("[INFO] Fetch success.")
    else:
        print("[ERROR] Failed to fetch.", returncode)
    return returncode

def _checkout_main():
    print("[INFO] Checking out main...")
    returncode = subprocess.run(["git", "checkout", "-f", "main"]).returncode
    if returncode == 0:
        print("[INFO] Switched to the main branch.")
    else:
        print("[ERROR] Failed to checkout the main branch. Return code:", returncode)
    return returncode

def _pull():
    print("[INFO] Pulling...")
    returncode = subprocess.run(["git", "pull"]).returncode
    if returncode == 0:
        print("[INFO] Pull success.")
    else:
        print("[ERROR] Failed to pull. Return code:", returncode)
    return returncode

def _setup():
    print("[INFO] Running the setup script...")
    returncode = -1
    match os.name:
        case 'nt':
            returncode = subprocess.run(["python", "setup.py"]).returncode
        case _:
            returncode = subprocess.run(["python3", "setup.py"]).returncode
    if returncode == 0:
        print("[INFO] Setup success.")
    else:
        print("[ERROR] Failed to run the setup script. Return code:", returncode)
    return returncode

def force_upgrade():
    return _discard_current() or _fetch() or _checkout_main() or _pull() or _setup() or 0

if __name__ == "__main__":
    print("VRChat Avi Scaler self-upgrade system.")
    print("[WARNING] This is an experimental feature. Things may go very wrong!")
    print("The program will be upgraded to the latest version from the main branch.")
    print("This only works if you cloned the repository (which is the recommended method) and did not delete the .git folder.")
    print("This WILL discard your modifications and quite possibly your config, and (re-)install the latest version, even if you're on the latest version.")
    if input("Please type y and press Enter to continue: ").strip() == "y":
        if force_upgrade() == 0:
            print("Upgrade success.")
        else:
            print("Upgrade failed. You may need to do a clean installation.")
    else:
        print("Cancelled.")
