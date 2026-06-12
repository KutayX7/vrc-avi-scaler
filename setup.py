import subprocess
import os
import sys
import argparse
from shutil import which
from pathlib import Path

if __name__ != "__main__":
    raise Exception("This can not be used as a module.")

venv_path = Path('.') / '.venv'
start_script_name: str = 'start.sh'

print(f"[INFO] Detected OS: {os.name}/{sys.platform}")

match os.name:
    case 'nt': # Windows
        pass
    case 'posix': # Linux | macOS | Android
        pass
    case _:
        print("[ERROR] Your operating system is not compatible with this program.")
        sys.exit(-1)

parser = argparse.ArgumentParser(
    prog = "vrc-avi-scaler-self-upgrade",
    description = "Upgrades the program to the latest version from the main branch."
)
parser.add_argument('-d', '--dev', action='store_true')
args = parser.parse_args()

requirements_file: str = 'requirements.txt'
if args.dev:
    requirements_file = 'requirements_dev.txt'

def install_dependencies() -> int:
    print("[INFO] Installing dependencies...")
    returncode = 0
    match os.name:
        case 'nt': # Windows
            process = subprocess.run([f"{venv_path}\\Scripts\\pip.exe", "install", "-r", f"{requirements_file}"])
            returncode = process.returncode
        case 'posix': # Linux
            process = subprocess.run([f"{venv_path}/bin/pip3", "install", "-r", f"{requirements_file}"])
            returncode = process.returncode
    if returncode == 0:
        print("[INFO] Dependency installation complete.")
    else:
        print("[ERROR] Dependency installation failed.")
    return returncode

def make_start_script_executable() -> int:
    if os.name != 'posix':
        return 0
    print(f"[INFO] Making {start_script_name} executable...")
    process = subprocess.run(["chmod", "+x",f"./{start_script_name}"])
    if process.returncode == 0:
        print(f"[INFO] {start_script_name} is now executable.")
    else:
        print(f"[ERROR] Failed to make {start_script_name} executable.")
    return process.returncode

def check_venv() -> int:
    print("[INFO] Checking for virtual environment...")
    if venv_path.exists():
        if venv_path.is_dir():
            print("[INFO] Found a virtual environment.")
            return 0
        else:
            print("[ERROR] Found a virtual environment but it's not a directory.'")
            return -1
    else:
        print("[INFO] Couldn't find a virtual environment.")
        return 0

def create_venv() -> int:
    print("[INFO] Creating a virtual environment...")
    match os.name:
        case 'nt':
            python_launcher_path = which('py')
            python_path = which('python')
            python3_path = which('python3')
            returncode = -1
            if python_launcher_path:
                returncode = subprocess.run(["py", "-3.13", "-m", "venv", ".venv"]).returncode
            elif python3_path:
                returncode = subprocess.run(["python3", "-m", "venv", ".venv"]).returncode
            elif python_path:
                returncode = subprocess.run(["python", "-m", "venv", ".venv"]).returncode
            else:
                print("[ERROR] Couldn't find python. Either something is wrong in the script or something is horribly wrong about your python installation (or both).")
            if returncode == 0:
                print("[INFO] Created a virtual environment.")
            else:
                print("[ERROR] Failed to create a virtual environment.")
            return returncode
        case _:
            returncode = subprocess.run(["python3", "-m", "venv", ".venv"]).returncode
            if returncode == 0:
                print("[INFO] Created a virtual environment.")
            else:
                print("[ERROR] Failed to create a virtual environment.")
            return returncode

if (check_venv() == 0 and
    create_venv() == 0 and
    install_dependencies() == 0 and
    make_start_script_executable() == 0):
    print("Installation complete.")
else:
    print("Installation failed.")
    sys.exit(-1)
