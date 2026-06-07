# KutayX7's VRChat Avi Scaler

A simple tool for advanced control of your avatar scale on VRChat.

## Features

- Uses OSC to communicate with VRChat.
- Scale your avatar to any size allowed by the world and VRChat.
- Option to scale instantly, or smoothly over a period of time.
- Compatibility with third-party scaling systems:
  * Full compatibility with [Jackal Scaling System](https://spacejackal.gumroad.com/l/JackalScaler).
  * Partial-compatibility with [Mag's Scale Adjuster](https://magww.gumroad.com/l/scale).
  * [OpenVRCScaler](https://github.com/SkyeCA/OpenVRCScaler) (coming soon)
  * [SizeOSC](https://anmeire.gumroad.com/l/sizeosc) (considering)
  * (More to be added.)
- Should work on Windows, Linux, macOS, Android/Quest (via Termux), and possibly on some other platforms.
  * But so far I only tested on Linux and Android.
- You can run VRChat and this program on separate devices.
  * Automatic connection with OSCQuery by default.
- Various commands, see [all commands](#all-commands).

> [!NOTE]
> A first-party scaling system (Unity/VCC prefab) is in development.
> A sample avatar to try it early: https://vrchat.com/home/avatar/avtr_afad73bf-ecfe-460a-b35b-6e77b29304b6
> (not complete yet but it's somewhat usable)

## Installation

> [!NOTE]
> Pretty much every step that apply to Linux should apply to macOS and Android (Termux) too.

### Prerequisites

* Internet connection.
* A terminal emulator (Pre-installed in almost all desktop operating systems. You can use Termux on Android/Quest.)
* Python (3.12+)
  - Windows users have to install this manually.
    - You can install it either from the [official Python website](https://www.python.org/downloads/windows/) or from the [Microsoft Store](https://apps.microsoft.com/detail/9pnrbtzxmb4z?ocid=webpdpshare).
    - If you see the option `Add to PATH` (or similar) during the installation, make sure it has been checked!
  - On Linux, it is pre-installed. But if you have an older version, I can't say if it will work or not. **DO NOT MANUALLY UPDATE YOUR SYSTEM PYTHON!**
  - You can check if python is installed and check its version by running
    - `python3 --version` or `python --version` (it's ok if at least one of them works)
* Git
  - Git is not required for the main functions of the program but it is required for the recommended installation method and for the update script to work.
  - Windows doesn't come with Git pre-installed but you can easily install Git by running `winget install --id Git.Git -e --source winget` then restarting your terminal.
  - Many linux distros come with git pre-installed. But if you don't have it, here are the commands to install it based on your linux distro.

      - Linux Mint / Pop!_OS / Ubuntu / Kubuntu / Debian

        ```bash
        sudo apt update && sudo apt install git
        ```

      - Fedora / Nobara

        ```bash
        sudo dnf install git
        ```

      - Arch Linux / SteamOS / Bazzite / CachyOS / EndeavourOS / Manjaro / Garuda

        ```bash
        sudo pacman -S git
        ```

      - Termux

        ```bash
        pkg install git
        ```

  - You can check if Git is installed and check its version by running `git --version`

### Recommended installation method

1. Open your terminal:
  * On Windows, `Win+R` and type `wt` (or `cmd`) then hit `Enter`
  * On Linux, it varies but usually `Crtl+Alt+T`
  * On Android, use Termux.
2. Clone the repository:
  * `git clone "https://github.com/KutayX7/vrc-avi-scaler"`
  * This will create the folder `vrc-avi-scaler` in the current directory (likely your home/user directory if you haven't moved into another directory)
    which will contain the `main` branch of this repository.
  * If you have already have that folder before running this (likely in the case of a previous version),
    this command will fail. So, please delete that folder before running this.
3. Change into the cloned directory:
  * `cd vrc-avi-scaler`
4. Run the setup script:
  * `python3 setup.py` or `python setup.py` or `py setup.py` (whichever works)
  * It will create a virtual environment (if it doesn't already exist).
  * Then it will install the dependencies in the virtual environment.
  * On Linux, it also makes the `start.sh` executable.

## Updates

There are no automatic updates nor check for updates, yet, so you'll have to update manually.

You can either do a clean installation (delete the whole `vrc-avi-scaler` folder and follow the recommended installation steps again) or run the `update.py` script.

Please check this README after each update.

## Usage

To start the program, run the start script:
  * On Windows, run the `start_windows.bat` script (you can double click it).
  * On Linux, run the `start.sh` script in your terminal.

Make sure to enable OSC in VRChat!

> [!WARNING]
> If you're already on VRChat before launching this or turning on the OSC, please reload your avatar (so it can collect accurate info about your avatar, tracking type, and the world).

> [!TIP]
> If you have issues with smooth scaling, limit your in-game FPS and use the `fps` command.
For example, if you set your in-game FPS limit to 120 FPS, use the command `fps 120`. Use the `save` command to save it so you don't have to type it later.

> [!TIP]
> Check `data/config.toml` for advanced configuration. If it doesn't exist, it will be generated when the program runs. You most probably never have to touch it though.

> [!TIP]
> By default, the config is not saved automatically. You can use the `autosave` command to make the config save automatically on exit.

## [Issues](https://github.com/KutayX7/vrc-avi-scaler/issues)

PLEASE GIVE FEEDBACK! That's the biggest support you could give for now. <3

All constructive feedback is welcome. Bug-reports, feature-requests, etc.
Please make sure you're using the latest version before opening a new issue (if applicable).
And please avoid making duplicate issues.

You can ask questions in [Q&A](https://github.com/KutayX7/vrc-avi-scaler/discussions/categories/q-a).

## Q&A

**Q: Is this safe?**

A: You can check the source code. The most dangerous parts are the dependencies and the experimental self-update. Also, if you're worried about getting moderated for using this, VRChat is unlikely to take any moderation action against you as long as you don't abuse it. This program does not use any illegal method.

**Q: Does it work on Android or Quest 2/3?**

A: If you're playing on Android/Quest it is recommended to run the app on a separate device. They should be able to connect automatically as long as they are on the same Wi-Fi network.

**Q: Why does smooth scaling make my avatar weird?**

A: It's probably related to these VRChat bugs:
  * https://feedback.vrchat.com/bug-reports/p/flicker-when-changing-avatar-height
  * https://feedback.vrchat.com/bug-reports/p/jittering-view-effect-when-lerping-osc-avatar-scaling
  * (I tried my best to mitigate them but the experience may not be perfect.)

**Q: Why not release packages/executables?**

A: This way felt more convenient to me and it makes it easy to update. You can use the `update.py` script to update the app easily once installed, and it should work on forks too without any modifications needed.

**Q: Any plans for a GUI?**

A: Not any plans for now. There are alternative apps with GUIs. Also, feel free to use this as the backend of your own GUI projects (but good luck with it as this is not designed for that).

**Q: Compatibility with X scaling system?**

A: This program is designed with compatibility in mind so open an issue about it and I will look into it. If you can give a public avatar that has it, and/or the parameters it uses, I can add it sooner.

**Q: Can I use other OSC apps along with this?**

A: Yes.

## All commands

- `<number>[unit]` Scales you to the specified eye height.
  - Valid examples: `1`, `173cm`, `2.1 m`, `200mm`, `1 mile`, `6ft`, `5000 feet`
  - Unit is `meters` if not specified.
- `smooth [seconds]` Sets smooth scaling duration.
  - Short version: `s [seconds]`
  - Not saved. Disabled by default.
- `help` Shows some of the most useful commands.
- `exit` Exits the app. Saves the config if `autosave` is on.
- `framerate <fps>` Sets the expected FPS.
  - Short version: `fps <fps>`
  - This also resets the `frequency`!
- `frequency <rate>` Sets the smooth scaling stepping rate (per second).
  - Short version: `freq <rate>`
  - Not saved.
- `clear` Clears the screen.
  - Short version: `cls`
- `save` Manually saves the current config. 
- `autosave` Enables autosave.
- `noautosave` Disables autosave.
- `min`/`max` Scales you to the min/max height set by world.
- `normal` Returns you to your normal height.
  - Short versions: `norm`, `base`
- `info` Shows various information about your avatar and world limits.
  - If mode (VR/desktop) is incorrectly detected, use the `vr` or `desktop` command.
- `vr` Selects VR mode.
- `desktop` Selects desktop mode.
  - Short version: `nvr`
- `osc_debug` Enables/disables OSC message logging.
- `osc_send <address> [params]` Sends a custom OSC message.
  - params: `<type>[value]`, examples: `i123 f0.5 T F`
  - Strings (`s`) are not supported.
  - Full example: `osc_send /avatar/eyeheight f0.5`
- `nocompat` Disables all scaling system compatibility features.
  - Short version: `pure`
  - Not saved.
- `override` Forgets world limits.
  - Only to get around some glitches. It won't make you bypass strict world limits.
  - Short version: `o`
- `instant` Disables smooth scaling.
  - Same as: `s 0`

## Disclaimer
> This project is neither affiliated with nor endorsed by VRChat nor by other avatar scaling system creators.
