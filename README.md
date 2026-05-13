# KutayX7's VRChat Avi Scaler
A simple command line tool to control your avatar height/scale on VRChat.

## Features
- Scale your avatar to any size allowed by the world and VRChat.
- Option to scale instantly, or over a period of time.
- Compatibility with 3rd-party scalers:
  * Full compatibility with [Jackal Scaling System](https://spacejackal.gumroad.com/l/JackalScaler).
  * Partial-compatibility with [Mag's Scale Adjuster](https://magww.gumroad.com/l/scale).

## Installation
### Prerequisites
* A terminal (pre-installed in almost all operating systems)
* Python (preferably 3.13 or newer)
* Git (the version control software)

> [!NOTE]
> While I'm not sure, most steps that apply to Linux should apply to Mac too.

> [!NOTE]
> Use `python3`/`pip3` if `python`/`pip` don't work (and vice versa).

### Recommended installation method
1. Open your Terminal:
  * On Windows, `Win+R` and type `wt` then hit `Enter`.
  * On Linux, it varies but usually `Crtl+Alt+T`.
2. Clone the repository:
  * `git clone "https://github.com/KutayX7/vrc-avi-scaler"`
  * This will create the folder `vrc-avi-scaler` (in your user home directory if you haven't moved to another directory)
    which will contain the `main` branch of this repository.
  * If you have already have that folder before running this (likely in the case of a previous version),
    this command will fail. So, please delete that folder before running this.
3. Change into the cloned directory:
  * `cd vrc-avi-scaler`
4. Create a virtual environment:
  * `python -m venv .venv`
5. Activate the virtual environment:
  * On Windows, `.venv\Scripts\activate`
  * On Linux, `source .venv/bin/activate`
6. Install the dependencies:
  * `pip install -r requirements.txt`

## Updates
There are no automatic updates nor check for updates, yet, so you'll have to update manually.

Clean (re-)install is recommended as there's currently no backwards compatibilty for the config files. Simply delete the whole `vrc-avi-scaler` folder and follow the installation steps again.

## Usage
To start the program:
1. Open your terminal in the same directory as `main.py`.
2. Activate the virtual environment.
3. `python main.py`

> [!WARNING]
> If you're already on VRChat before launching this, it is *recommended* to rejoin the instance (so it can collect accurate info about your avatar and the world).

> [!TIP]
> Check `config.ini` and `globals.py` for advanced configuration.

## Issues
All constructive feedback is welcome.

## Disclaimer
> This project is neither affiliated with nor endorsed by VRChat and other avatar scaler creators.
