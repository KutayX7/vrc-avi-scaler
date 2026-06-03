import subprocess
import os
import sys
import fs
from pathlib import Path

venv_path = './.venv'
python_name = 'python'
start_script_name = 'start.sh'

print(f"[INFO] Detected OS: {os.name}/{sys.platform}")

match os.name:
	case 'nt': # Windows
		venv_name = '.\\.venv'
	case 'posix': # Linux
		python_name = 'python3'
	case _:
		raise Exception("unknown/unsupported operating system")

def install_dependencies():
	print("[INFO] Installing dependencies...")
	returncode = 0
	match os.name:
		case 'nt': # Windows
			process = subprocess.run(f"{venv_path}\\Scripts\\pip.exe install -r requirements.txt", shell=True)
			returncode = process.returncode
		case 'posix': # Linux
			process = subprocess.run(f"{venv_path}/bin/pip3 install -r requirements.txt", shell=True)
			returncode = process.returncode
	if returncode == 0:
		print("[INFO] Dependency installation complete.")
	else:
		print("[ERROR] Dependency installation failed.")
	return returncode

def make_start_script_executable():
	if os.name != 'posix':
		return 0
	print(f"[INFO] Making {start_script_name} executable...")
	process = subprocess.run(f"chmod +x ./{start_script_name}", shell=True)
	if process.returncode == 0:
		print(f"[INFO] {start_script_name} is now executable.")
	else:
		print(f"[ERROR] Failed to make {start_script_name} executable.")
	return process.returncode

def create_venv():
	print("[INFO] Checking for virtual environment...")
	venv = Path(venv_path)
	if venv.exists():
		if venv.is_dir():
			print("[INFO] Found a virtual environment.")
			return 0
		else:
			print("[ERROR] Found a virtual environment but it's not a directory.'")
			return -1
	else:
		print("[INFO] Couldn't find a virtual environment.")
		print("[INFO] Creating a virtual environment...")
		process = subprocess.run(f"{python_name} -m venv .venv", shell=True)
		if process.returncode == 0:
			print("[INFO] Created a virtual environment.")
		else:
			print("[ERROR] Failed to create a virtual environment.")
		return process.returncode

if __name__=="__main__":
	if (create_venv() == 0 and
		install_dependencies() == 0 and
		make_start_script_executable() == 0):
		print("Installation complete.")
	else:
		print("Installation failed.")
		sys.exit(-1)
