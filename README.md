# KutayX7's VRChat Avi Scaler
A simple command line tool to control your avatar height/scale on VRChat.

## Features
- Scale your avatar to any size allowed by the world and VRChat.
- Option to scale instantly, or smoothly over a period of time.
- Compatibility with third-party scaling systems:
  * Full compatibility with [Jackal Scaling System](https://spacejackal.gumroad.com/l/JackalScaler).
  * Partial-compatibility with [Mag's Scale Adjuster](https://magww.gumroad.com/l/scale).
- Should work on Windows, Linux, Quest/Android (via Termux), and possibly on some other platforms.
  * (But so far I only tested on Linux and Android.)

> [!NOTE]
> A first-party scaling system (the Unity/VCC package) is in development.
> A sample avatar to try it early: https://vrchat.com/home/avatar/avtr_afad73bf-ecfe-460a-b35b-6e77b29304b6
> (not feature complete yet but it's usable)

## Installation
### Prerequisites
* A terminal emulator (Pre-installed in almost all desktop operating systems. You can use Termux on Quest/Android.)
* Python (3.13+)
* Git (the version control software)

> [!NOTE]
> Most steps that apply to Linux should apply to Mac and Android (Termux) too.

### Recommended installation method
1. Open your Terminal:
  * On Windows, `Win+R` and type `wt` then hit `Enter`
  * On Linux, it varies but usually `Crtl+Alt+T`
  * On Android, use Termux.
2. Clone the repository:
  * `git clone "https://github.com/KutayX7/vrc-avi-scaler"`
  * This will create the folder `vrc-avi-scaler` (likely in your user home directory if you haven't moved into another directory)
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

## Usage
To start the program, run the start script:
  * On Windows, double click on `start_windows.bat`.
  * On Linux, run the `start.sh` script.

Type `help` to see a list of commands.

It's recommended to limit your in-game FPS and use the `fps` command after each launch.
For example, if you set your in-game FPS limit to 90 FPS, use the command `fps 90`.

Make sure to enable OSC in VRChat!

> [!WARNING]
> If you're already on VRChat before launching this or enabling OSC, it is *recommended* to rejoin the instance (so it can collect accurate info about your avatar, tracking type, and the world).

> [!TIP]
> Check `globals.py` for advanced configuration.

## [Issues](https://github.com/KutayX7/vrc-avi-scaler/issues)
PLEASE GIVE FEEDBACK! That's the biggest support you could give for now. <3

All constructive feedback is welcome. Bug-reports, feature-requests, etc.
Please make sure you're using the latest version before opening a new issue (if applicable).
And please avoid making duplicate issues.

## Q&A
**Q: Is this safe?**

A: You can check the source code. The most dangerous part is the installation of dependencies. Also, if you're worried about getting moderated for using this, VRChat is unlikely take any moderation action against you as long as you don't abuse it. This program does not use any illegal method.

**Q: Why does smooth scaling makes my avatar flicker on desktop?**

A: You most likely haven't used the `fps` command correctly. Though, if you did, you're likely dealing with the fake jitter feature, which is a workaround I made to reduce the effects of another bug (https://feedback.vrchat.com/bug-reports/p/flicker-when-changing-avatar-height).
   But in case that bug gets fixed and I no longer can develop the program, just set `smooth_scaling_jitter_range` to `0.0` in `globals.py`, or use the `jitter` command.

**Q: I don't want to use the `fps` command every time.**

A: Set `FPS` in `globals.py` to your FPS cap. (If VRChat makes an update that exposes FPS information over OSC, I will make this automatic.)

## Disclaimer
> This project is neither affiliated with nor endorsed by VRChat nor by other avatar scaling system creators.
