import threading
import time

import globals
import compat
import client
import server
import scaling_utils

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
                 (defaults to 3 seconds if not specified)

    fps <rate> : Sets the expected in-game frame-rate.
                 Since this program can't directly read your in-game frame-rate
                 (at least not yet) it can make bad assumptions
                 which can result in more visual glitches.
                 This commands allows you to tell your in-game frame-rate
                 to make better decisions.
                 It is recommended to cap your FPS in-game.

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
        globals.world_min_eyeheight = globals.MIN_HEIGHT
        globals.world_max_eyeheight = globals.MAX_HEIGHT
        globals.world_scaling_allowed = True
        print("Forgot the world limits ;)")
        print("You may encounter weird behavior.")
    elif command == "instant":
        globals.smooth_scaling_duration = 0
    elif command == "smooth" or command == "s":
        try:
            length = abs(float(tokens[1]))
        except:
            length = 3.0
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
    elif command == "jitter":
        if len(tokens) == 1:
            if globals.smooth_scaling_jitter_range > 0:
                globals.smooth_scaling_jitter_range = 0.0
            else:
                globals.smooth_scaling_jitter_range = 0.002
        else:
            try:
                jitter_range = abs(float(tokens[1]))
                globals.smooth_scaling_jitter_range = jitter_range
            except:
                pass
        if globals.smooth_scaling_jitter_range > 0:
            print(f"Smooth scaling jitter range set to ±{globals.smooth_scaling_jitter_range}")
        else:
            print("Smooth scaling jitter disabled.")
    else:
        try:
            desired_height = float(command)
        except:
            print("Unknown command. You can type \"help\" for a list of commands.")
    if desired_height != globals.current_eyeheight:
        if globals.world_scaling_allowed:
            if desired_height < globals.MIN_HEIGHT:
                print(f"Too small! Minimum {globals.MIN_HEIGHT} m.")
            elif desired_height > globals.MAX_HEIGHT:
                print(f"Too big! Maximum {globals.MAX_HEIGHT} m.")
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
    globals.server = server.start_server(globals.osc_server_ip, globals.osc_server_port)
    globals.client = client.start_client(globals.osc_client_ip, globals.osc_client_port)
    print("")
    while True:
        process_command(input(""))

if __name__ == "__main__":
    main()
