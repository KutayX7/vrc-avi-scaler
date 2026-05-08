import threading
import configparser
import time

import globals
import compat
import client
import server
import scaling_utils

config = configparser.ConfigParser()
config.read('config.ini')

DEFAULT_SERVER_IP =       config['OSC server']['ip']
DEFAULT_CLIENT_IP =       config['OSC client']['ip']
DEFAULT_SERVER_PORT = int(config['OSC server']['port'])
DEFAULT_CLIENT_PORT = int(config['OSC client']['port'])
MIN_HEIGHT = float(config['limits']['MinHeight'])
MAX_HEIGHT = float(config['limits']['MaxHeight'])
globals.MIN_HEIGHT = MIN_HEIGHT
globals.MAX_HEIGHT = MAX_HEIGHT

globals.compat_magsscaleadjuster = bool(int(config['compatibility']['MagsScaleAdjuster']))

help_text = """Available commands:
    quit  : Quits the app.
    exit

    info  : Shows various information about your size and limits.
    i

    min   : Sets your height to the minimum height set by the world.
    max   : Sets your height to the maximum height set by the world.
    base  : Sets your height to the original size of your avatar.

    override   : Makes the app forget the world limitations.
    o

    instant    : Makes scaling instant. (default behavior)
    smooth [t] : Makes scaling not instant.
    s            You can also set a duration in seconds as the second argument.
                 (defaults to 5 seconds if not specified)

    fps [rate] : Sets the expected in-game frame-rate.
                 Since this program can't directly read your in-game frame-rate
                 (at least not yet) it can make bad assumptions
                 which can result in more visual glitches.
                 This commands allows you to tell your in-game frame-rate
                 so that the program can make better assumptions.
                 It is recommended to cap your FPS.

To change your size, just type your desired eye height (in meters).
Do NOT add unit suffixes! They are not supported, for now."""

def process_command(full_command):
    tokens = full_command.split()
    if len(tokens) < 1:
        return
    client = globals.client
    height = globals.current_eyeheight
    command = tokens[0]
    desired_height = height
    if command == "quit" or command == "exit":
        quit()
    elif command == "help":
        print(help_text)
    elif command == "min":
        desired_height = globals.world_min_eyeheight
    elif command == "max":
        desired_height = globals.world_max_eyeheight
    elif command == "base":
        desired_height = scaling_utils.get_base_eyeheight()
    elif command == "info" or command == "i":
        print("Avatar:")
        if globals.current_eyeheight > 0:
            print("  Calculated base eye height:", scaling_utils.get_base_eyeheight(), 'm')
            print("  Current eye height:", globals.current_eyeheight, 'm')
            print("  Current scale factor:", globals.current_scale_factor)
        else:
            print("  Height data not available.")
            print("  Please reload your avatar, or change your height manually.")
        if globals.smooth_scaling_duration > 0:
            print("  Smooth scaling is enabled.")
            print(f"    Duration: {globals.smooth_scaling_duration} s")
            print(f"    Frequency: {globals.smooth_scaling_step_frequency} hz")
            print(f"    Jitter: ±{globals.smooth_scaling_jitter_range}")
            if globals.smooth_scaling_jitter_range > 0:
                print("    Some fake jitter is added to keep more annoying visual glitches at bay.")
                print("    You can lower/disable this effect in globals.py if it really bothers you.")
                print("      (Requires restart if you change it)")
        else:
            print("  Smooth scaling is disabled. (Instant scaling mode.)")
        if globals.world_scaling_allowed:
            print("World limits:")
            if (globals.world_min_eyeheight == 0 and
                globals.world_max_eyeheight == 0):
                print("  World limits are unknown.")
                print("  Please rejoin the instance (or use the override command).")
            else:
                print("  Min eye height: ", globals.world_min_eyeheight, 'm')
                print("  Max eye height: ", globals.world_max_eyeheight, 'm')
                print("  Note: You may be able to go over these limits.")
                print("        Only some worlds actually enforce them.")
        else:
            print("Avatar scaling is currently disabled by the world.")
    elif command == "override" or command == "o":
        globals.world_min_eyeheight = MIN_HEIGHT
        globals.world_max_eyeheight = MAX_HEIGHT
        globals.world_scaling_allowed = True
        print("Forgot the world limits ;)")
        print("You may encounter weird behavior.")
    elif command == "instant":
        globals.smooth_scaling_duration = 0
    elif command == "smooth" or command == "s":
        try:
            length = abs(float(tokens[1]))
        except:
            length = 5.0
        finally:
            if globals.smooth_scaling_duration <= 0:
                print(f"Enabled smooth scaling.")
            globals.smooth_scaling_duration = length
            print(f"Smooth scaling duration set to {length} s.")
            if globals.current_eyeheight == 0:
                print("Please reload your avatar!")
    elif command == "fps":
        try:
            fps = abs(float(tokens[1]))
            globals.FPS = fps
            globals.smooth_scaling_step_frequency = fps * 4
            print(f"Epected FPS set to {fps}")
        except:
            pass
    elif command == "frequency" or command == "freq":
        try:
            frequency = abs(float(tokens[1]))
            globals.smooth_scaling_step_frequency = frequency
            print(f"Smooth scaling step frequency set to {frequency}")
        except:
            pass
    else:
        try:
            desired_height = float(command)
        except:
            print("Unknown command. You can type \"help\" for a list of commands.")
    if desired_height != globals.current_eyeheight:
        if globals.world_scaling_allowed:
            if desired_height < MIN_HEIGHT:
                print(f"Too small! Minimum {MIN_HEIGHT} m.")
            elif desired_height > MAX_HEIGHT:
                print(f"Too big! Maximum {MAX_HEIGHT} m.")
            else:
                client.set_eyeheight(desired_height, globals.smooth_scaling_duration)
        else:
            print("Avatar scaling is not available right now.")

def main():
    print("\033[0;33m[ KutayX7's VRChat Avi Scaler ]\033[0m")
    print("For issues and feedback, visit https://github.com/KutayX7/vrc-avi-scaler/issues")
    print("Type \"help\" to see a list of commands.")
    print("Type \"quit\" to quit.")
    print("--------------------")
    globals.server = server.start_server(DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT)
    globals.client = client.start_client(DEFAULT_CLIENT_IP, DEFAULT_CLIENT_PORT)
    print("")
    while True:
        process_command(input(""))

if __name__ == "__main__":
    main()
