import subprocess
import os
import argparse

CURRENT: str = "current"
branch: str = CURRENT

def _discard_unstaged() -> int:
    print("[INFO] Discarding unstaged changes...")
    returncode: int = subprocess.run(["git", "checkout", "."]).returncode
    if returncode == 0:
        print("[INFO] Discarded unstaged changes.")
    else:
        print("[ERROR] Failed to discard unstaged changes. Return code:", returncode)
    return returncode

def _discard_staged() -> int:
    print("[INFO] Discarding staged changes...")
    returncode: int = subprocess.run(["git", "reset", "--hard", "HEAD"]).returncode
    if returncode == 0:
        print("[INFO] Discarded staged changes.")
    else:
        print("[ERROR] Failed to discard staged changes. Return code:", returncode)
    return returncode

def _discard_current() -> int:
    return _discard_unstaged() or _discard_staged() or 0

def _fetch() -> int:
    print("[INFO] Fetching...")
    returncode: int = subprocess.run(["git", "fetch"]).returncode
    if returncode == 0:
        print("[INFO] Fetch success.")
    else:
        print("[ERROR] Failed to fetch.", returncode)
    return returncode

def _checkout(branch: str) -> int:
    if branch == CURRENT:
        print(f"[INFO] Staying on the same branch.")
        return 0
    print(f"[INFO] Trying to checkout {branch}...")
    returncode: int = subprocess.run(["git", "checkout", "-f", branch]).returncode
    if returncode == 0:
        print(f"[INFO] Successfully switched to {branch}")
    else:
        print(f"[ERROR] Failed to checkout the {branch} branch. Return code:", returncode)
    return returncode

def _pull() -> int:
    print("[INFO] Pulling...")
    returncode: int = subprocess.run(["git", "pull"]).returncode
    if returncode == 0:
        print("[INFO] Pull success.")
    else:
        print("[ERROR] Failed to pull. Return code:", returncode)
    return returncode

def _setup() -> int:
    print("[INFO] Running the setup script...")
    returncode: int = -1
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

def force_upgrade(branch: str = CURRENT) -> int:
    return (_discard_current() or
            _fetch() or
            _checkout(branch) or
            _pull() or
            _setup() or
            0)

def _validate_branch_name(branch: str) -> bool:
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-0123456789"
    for char in branch:
        if char in chars:
            pass
        else:
            return False
    return len(branch) < 100 and len(branch) > 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "VRChat Avi Scaler self-upgrade",
        description = "Updates the program to the latest version.",
    )
    parser.add_argument("-b", "--branch", default=CURRENT)
    parser.add_argument("-y", "--yes", default=False)
    args = parser.parse_args()
    branch = args.branch

    if not _validate_branch_name(branch):
        print("[WARNING] Invalid branch name.")
        branch = CURRENT

    print( "VRChat Avi Scaler self-upgrade system.")
    print( "[WARNING] This is an experimental feature. Things may go very wrong!")
    print(f"The program will be upgraded to the latest version from the {branch} branch.")
    print( "This only works if you cloned the repository and did not delete the .git folder.")
    print( "This WILL discard your modifications and quite possibly your config, and (re-)install the latest version, even if you're on the latest version already.")
    if args.yes or input("Please type y and press Enter to continue: ").strip() == "y":
        if force_upgrade(branch=branch) == 0:
            print("Upgrade success.")
        else:
            print("Upgrade failed. You may need to do a clean installation.")
    else:
        print("Cancelled.")
