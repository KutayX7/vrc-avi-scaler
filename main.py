import sys
import globals
import client
import server
import oscquery
from config import *
from simple_types import ParameterValue, Height
from scaling_utils import get_base_eyeheight, parse_to_meters, is_valid_float

help_text: str = """
Available commands:
    quit   : Quits the app.
    exit

    clear  : Clears the terminal screen.
    cls

    info   : Shows various information about your size and limits.
    i

    normal : Sets your height to the original size of your avatar.
    norm
    base

    instant    : Makes scaling instant.
                 Same effect as `s 0`
    smooth [t] : Makes scaling not instant.
    s            You can also set a duration in seconds as the second argument.
                 Defaults to 3 seconds if not specified.

    fps <value> : Sets the expected in-game frame-rate.
                  Since this program can't directly read your in-game frame-rate
                  (at least not yet) it can make bad assumptions
                  which can result in more visual glitches or instabilities.
                  This commands allows you to tell your in-game frame-rate
                  to make better decisions.
                  It is recommended to cap your FPS in-game.

    autosave : Turns on autosave which saves the
               current configuration on exit.

To change your size, just type your desired eye height (optionally with the unit)."""

def shutdown() -> None:
    print("Shutting down the program...")
    if globals.save_config_on_exit:
        save_config()
    print("Feel free to close the window/terminal.")
    sys.exit(0)

def check_float(value: float) -> None:
    if not is_valid_float(value):
        raise Exception()

def process_command(full_command: str) -> None:
    tokens = full_command.split()
    if len(tokens) < 1:
        return
    client = globals.client
    height: Height = globals.current_eyeheight
    command: str = tokens[0]
    desired_height: Height = height
    match command:
        case "quit" | "exit":
            shutdown()
        case "help":
            print(help_text)
        case "clear" | "cls":
            print("\033[3J\033[H\033[2J", end="")
        case "min":
            desired_height = globals.world_min_eyeheight
        case "max":
            desired_height = globals.world_max_eyeheight
        case "normal" | "reset" | "norm" | "base":
            desired_height = get_base_eyeheight()
        case "vr":
            globals.VRMode = True
        case "desktop" | "nonvr" | "novr" | "nvr":
            globals.VRMode = False
        case "nocompat" | "pure":
            globals.compat_killswitch = True
        case "client_fix":
            detected_ip: str = globals.osc_detected_VRChat_ip
            current_ip: str = client.ip
            if detected_ip and detected_ip != current_ip:
                client.reconnect(detected_ip, client.port)
        case "osc_debug":
            globals.osc_debug_log = not globals.osc_debug_log
            if globals.osc_debug_log:
                print("Enabled OSC debugging.")
            else:
                print("Disabled OSC debugging.")
        case "osc_send":
            address: str = tokens[1]
            list_to_send: list[ParameterValue] = []
            for token in tokens[2:]:
                token_type = token[0:1]
                match token_type:
                    case 'i':
                        list_to_send.append(int(token[1:]))
                    case 'f':
                        list_to_send.append(float(token[1:]))
                    case 'T':
                        list_to_send.append(True)
                    case 'F':
                        list_to_send.append(False)
                    case 's':
                        print("Can't parse strings.")
                        return
            print(f"Sending OSC message: {address} {list_to_send}")
            client.send_message(address, list_to_send)
        case "info" | "i":
            print("Avatar:")
            if globals.current_eyeheight > 0:
                if globals.VRMode:
                    print( "  Mode: VR")
                    print(f"  TrackingType: {globals.tracking_type} point tracking")
                else:
                    print("  Mode: Desktop")
                print(f"  Calculated base eye height: {get_base_eyeheight()} m")
                print(f"  Current eye height: {globals.current_eyeheight} m")
                print(f"  Current scale factor: {globals.current_scale_factor}")
            else:
                print( "  Height data not available.")
                print( "  Please reload your avatar, or change your height manually.")
            if globals.smooth_scaling_duration > 0:
                print( "  Smooth scaling is enabled.")
                print(f"    Duration: {globals.smooth_scaling_duration} s")
                print(f"    Frequency: {globals.smooth_scaling_step_frequency} hz")
            else:
                print( "  Smooth scaling is disabled. (Instant scaling mode.)")
            if globals.world_scaling_allowed:
                print("World limits:")
                if (globals.world_min_eyeheight == 0 and
                    globals.world_max_eyeheight == 0):
                    print( "  World limits are unknown.")
                    print( "  Please reload your avatar. Tip: toggle OSC off then on.")
                else:
                    print(f"  Min eye height: {globals.world_min_eyeheight} m")
                    print(f"  Max eye height: {globals.world_max_eyeheight} m")
                    print( "  Note: You may be able to go over these limits.")
                    print( "        Only some worlds actually enforce them.")
            else:
                print("Avatar scaling is currently disabled by the world.")
        case "override" | "o":
            globals.world_min_eyeheight = globals.MIN_EYEHEIGHT
            globals.world_max_eyeheight = globals.MAX_EYEHEIGHT
            globals.world_scaling_allowed = True
            print("Forgot the world limits ;)")
            print("You may encounter weird behavior.")
        case "instant":
            globals.smooth_scaling_duration = 0
        case "smooth" | "s":
            length: float = globals.smooth_scaling_default_duration
            try:
                length = abs(float(tokens[1]))
                check_float(length)
            except:
                print(f"Duration is unspecified/invalid.")
            finally:
                if globals.smooth_scaling_duration <= 0:
                    print(f"Enabled smooth scaling.")
                globals.smooth_scaling_duration = length
                print(f"Smooth scaling duration set to {length} s.")
                if globals.current_eyeheight == 0:
                    print("Please reload your avatar!")
        case "framerate" | "fps":
            try:
                fps = abs(float(tokens[1]))
                check_float(fps)
                globals.FPS = fps
                globals.smooth_scaling_step_frequency = fps * 4
                print(f"Epected FPS set to {fps}")
            except:
                print("Invalid value.")
        case "frequency" | "freq":
            try:
                if len(tokens) == 1:
                    pass
                elif tokens[1] == "reset":
                    globals.smooth_scaling_step_frequency = globals.FPS * 4
                else:
                    frequency = abs(float(tokens[1]))
                    check_float(frequency)
                    globals.smooth_scaling_step_frequency = frequency
            except:
                print("Invalid value.")
            finally:
                print(f"Smooth scaling step frequency set to {globals.smooth_scaling_step_frequency} hz")
        case "save":
            save_config()
        case "autosave":
            globals.save_config_on_exit = True
            print("Turned on autosave.")
            print("The current configuration will be saved on exit.")
            print("You can use the `noautosave` command to turn off autosave.")
        case "manuelsave" | "manualsave" | "noautosave":
            globals.save_config_on_exit = False
            print("Turned off autosave.")
            print("You can save the current configuration manually by using the `save` command.")
        case _:
            try:
                desired_height = parse_to_meters(full_command, height)
            except:
                print("Unknown command. You can type \"help\" for a list of commands.")
    if desired_height != globals.current_eyeheight:
        if globals.world_scaling_allowed:
            if desired_height < globals.MIN_EYEHEIGHT:
                print(f"Too small! Minimum {globals.MIN_EYEHEIGHT} m.")
            elif desired_height > globals.MAX_EYEHEIGHT:
                print(f"Too big! Maximum {globals.MAX_EYEHEIGHT} m.")
            else:
                print(f"Setting eye height to {desired_height} m...")
                client.set_eyeheight(desired_height, globals.smooth_scaling_duration)
        else:
            print("Avatar scaling is not available right now.")

def main() -> None:
    print("\033[0;33m[ KutayX7's VRChat Avi Scaler ]\033[0m")
    print("For issues and feedback, visit https://github.com/KutayX7/vrc-avi-scaler/issues")

    config_read_result = read_config()
    match config_read_result:
        case ConfigReadResult.SUCCESS:
            pass
        case ConfigReadResult.NOT_FOUND:
            print("Config file not found. Creating one...")
            reset_config_file()
        case ConfigReadResult.ACCESS_DENIED:
            print("Could not access the config file. Access denied.")
            sys.exit(-1)
        case ConfigReadResult.CORRUPTED:
            print("Config file seems to be corrupted.")
            print("Would you like to reset it?")
            print("Options: yes | no")
            choice = input("?> ")
            match choice.lower():
                case "yes" | "y":
                    reset_config_file()
                case "no" | "n":
                    print("Would you like to contine with the default config?")
                    print("This will not overwrite the config file.")
                    print("Options: yes | no")
                    choice = input("?> ")
                    match choice.lower():
                        case "yes" | "y":
                            pass
                        case _:
                            shutdown()
                case _:
                    print("Invalid choice.")
                    sys.exit(-1)

    print("--------------------")
    print("Type \"help\" to see a list of commands.")
    print("Type \"quit\" to quit.")
    print("--------------------")
    osc_server_ip = globals.osc_server_ip
    osc_server_port = globals.osc_server_port
    if globals.oscquery_enabled:
        oscquery.start_service()
        oscquery.start_listener()
        osc_server_ip = ''
        osc_server_port = globals.oscquery_service_port
    globals.server = server.start_server(osc_server_ip, osc_server_port)
    globals.client = client.start_client(globals.osc_client_ip, globals.osc_client_port)

    while True:
        process_command(input(""))

if __name__ == "__main__":
    main()
