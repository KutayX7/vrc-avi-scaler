import subprocess
from argparse import ArgumentParser
from curses.ascii import iscntrl
from shutil import which

CURRENT: str = "current"
MAIN: str = "main"
branch: str = CURRENT
yes = False

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

def _change_branch(branch_name: str) -> int:
    global branch
    branch = branch_name
    return _checkout(branch)

def _change_branch_and_pull(branch: str) -> int:
    return _change_branch(branch) or _pull() or 0

def _pull() -> int:
    print("[INFO] Pulling...")
    returncode: int = subprocess.run(["git", "pull"]).returncode
    if returncode == 0:
        print("[INFO] Pull success.")
    else:
        print("[ERROR] Failed to pull. Return code:", returncode)
        if branch != MAIN:
            print("[INFO]: Requested branch may not exist anymore.")
            if yes:
                return _change_branch_and_pull(MAIN)
            else:
                print(f"Would you like to switch to the {MAIN} branch instead?")
                if input("y/N > ").strip() == 'y':
                    return _change_branch_and_pull(MAIN)
    return returncode

def _setup() -> int:
    print("[INFO] Locating python...")
    python_path = which('python3') or which('python') or "python3"
    print("[INFO] Found: ", python_path)
    print("[INFO] Running the setup script...")
    returncode: int = -1
    returncode = subprocess.run([python_path, "setup.py"]).returncode
    if returncode == 0:
        print("[INFO] Setup success.")
    else:
        print("[ERROR] Failed to run the setup script. Return code:", returncode)
    return returncode

def force_upgrade(*, branch: str = CURRENT) -> int:
    return (_discard_current() or
            _fetch() or
            _change_branch_and_pull(branch) or
            _setup() or
            0)

def _is_full_commit_hash(string: str) -> bool:
    if len(string) == 40:
        hex_chars = "0123456789ABCDEFabcdef"
        for char in string:
            if char not in hex_chars:
                return False
        return True
    else:
        return False

def _validate_branch_name(branch: str) -> bool:
    forbidden_chars = " ~^*:?[\\"
    if not branch:
        return False
    if branch == "@":
        return False
    for char in branch:
        if char in forbidden_chars:
            return False
        if iscntrl(char):
            return False
    if ".." in branch:
        return False
    if "/." in branch:
        return False
    if "//" in branch:
        return False
    if "@{" in branch:
        return False
    if branch.startswith("refs/"):
        return False
    if branch.endswith(".lock"):
        return False
    if branch[0] == "-":
        return False
    if branch[0] == "." or branch[-1] == ".":
        return False
    if branch[0] == "/" or branch[-1] == "/":
        return False
    if branch in ["HEAD", "FETCH_HEAD", "ORIG_HEAD", "MERGE_HEAD"]:
        return False
    if _is_full_commit_hash(branch):
        return False
    return True

if __name__ == "__main__":
    parser = ArgumentParser(
        prog = "VRChat Avi Scaler self-upgrade",
        description = "Updates the program to the latest version.",
    )
    parser.add_argument("-b", "--branch", default=CURRENT)
    parser.add_argument("-y", "--yes", action='store_true')
    args, _ = parser.parse_known_args()
    branch = args.branch
    yes = args.yes
    if not _validate_branch_name(branch):
        print("[WARNING] Invalid branch name.")
        branch = CURRENT
    print( "VRChat Avi Scaler self-upgrade system.")
    print(f"The program will be upgraded to the latest version from the {branch} branch.")
    print( "This only works if you cloned the repository and did not delete the .git folder.")
    print( "This WILL discard your modifications and quite possibly your config, and (re-)install the latest version on that branch, even if you're on the latest version already.")
    if yes or input("Please type y and press Enter to continue: ").strip() == "y":
        if force_upgrade(branch=branch) == 0:
            print("Upgrade success.")
        else:
            print("Upgrade failed. You may need to do a clean installation.")
    else:
        print("Cancelled.")
