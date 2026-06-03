# KutayX7's VRChat Avi Scaler
A simple tool for advanced control of your avatar scale on VRChat.

## Features
- Scale your avatar to any size allowed by the world and VRChat.
- Option to scale instantly, or smoothly over a period of time.
- Compatibility with third-party scaling systems:
  * Full compatibility with [Jackal Scaling System](https://spacejackal.gumroad.com/l/JackalScaler).
  * Partial-compatibility with [Mag's Scale Adjuster](https://magww.gumroad.com/l/scale).
- Should work on Windows, Linux, macOS, Quest/Android (via Termux), and possibly on some other platforms.
  * (But so far I only tested on Linux and Android.)

> [!NOTE]
> A first-party scaling system (Unity/VCC prefab) is in development.
> A sample avatar to try it early: https://vrchat.com/home/avatar/avtr_afad73bf-ecfe-460a-b35b-6e77b29304b6
> (not complete yet but it's somewhat usable)

## Installation
### Prerequisites
* Internet connection.
* A terminal emulator (Pre-installed in almost all desktop operating systems. You can use Termux on Android/Quest.)
* Python (3.13+)
* Git (the version control software)

> [!NOTE]
> Most steps that apply to Linux should apply to macOS and Android (Termux) too.

### Recommended installation method
1. Open your Terminal:
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
  * On Windows, `python setup.py`
  * On Linux, `python3 setup.py`

## Updates
There are no automatic updates nor check for updates, yet, so you'll have to update manually.

Clean (re-)install is recommended as there's currently no backwards compatibilty for the config files. Simply delete the whole `vrc-avi-scaler` folder and follow the installation steps again.

It's recommended to check this README after each update. :)

### Self-upgrade script (experimental)
There's a `update.py` script that *should* be able to update the program to the latest version from the main branch. I wasn't able to test it. Use it at your own risk! Please report any bugs and issues if you use it!

## Usage
To start the program, run the start script:
  * On Windows, double click on `start_windows.bat`.
  * On Linux, run the `start.sh` script.

Make sure to enable OSC in VRChat!

Type `help` to see a list of the most useful commands. (Check `main.py` for the full list of commands.)

If you have issues with smooth scaling, limit your in-game FPS and use the `fps` command.
For example, if you set your in-game FPS limit to 120 FPS, use the command `fps 120`.

> [!WARNING]
> If you're already on VRChat before launching this or turning on the OSC, it is *recommended* to reload your avatar (so it can collect accurate info about your avatar, tracking type, and the world).

> [!TIP]
> Check `data/config.toml` for advanced configuration. If it doesn't exist, it will be generated when the program runs.

> [!TIP]
> By default, the config is not saved automatically. You can use the `autosave` command to make the config save automatically on exit.

## [Issues](https://github.com/KutayX7/vrc-avi-scaler/issues)
PLEASE GIVE FEEDBACK! That's the biggest support you could give for now. <3

All constructive feedback is welcome. Bug-reports, feature-requests, etc.
Please make sure you're using the latest version before opening a new issue (if applicable).
And please avoid making duplicate issues.

## Q&A
**Q: Is this safe?**

A: You can check the source code. The most dangerous parts are the dependencies and handling of the config file (and the experimental self-update). Also, if you're worried about getting moderated for using this, VRChat is unlikely to take any moderation action against you as long as you don't abuse it. This program does not use any illegal method.

**Q: Why does smooth scaling make my avatar weird?**

A: It's probably related to these VRChat bugs:
  * https://feedback.vrchat.com/bug-reports/p/flicker-when-changing-avatar-height
  * https://feedback.vrchat.com/bug-reports/p/jittering-view-effect-when-lerping-osc-avatar-scaling
  (I tried my best to mitigate them but the experience is not perfect.)

## Disclaimer
> This project is neither affiliated with nor endorsed by VRChat nor by other avatar scaling system creators.
