import json
import threading
import configparser
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

config = configparser.ConfigParser()
config.read('config.ini')

DEFAULT_SERVER_IP =       config['OSC server']['ip']
DEFAULT_CLIENT_IP =       config['OSC client']['ip']
DEFAULT_SERVER_PORT = int(config['OSC server']['port'])
DEFAULT_CLIENT_PORT = int(config['OSC client']['port'])
MIN_HEIGHT = float(config['limits']['MinHeight'])
MAX_HEIGHT = float(config['limits']['MaxHeight'])

world_min = 0
world_max = 0
world_scaling_allowed = True
current_eyeheight = 0.0
current_scale_factor = 0.0
scaling_duration = 0.0
scaling = False
accurate = False

client = None
server = None

def float_range(start, stop, step):
    if step >= 0:
        while start < stop:
            yield start
            start += step
    else:
        while start > stop:
            yield start
            start += step

def get_base_eyeheight():
    if current_scale_factor == 0:
        return 0
    return current_eyeheight / current_scale_factor

def eyeheight_min_handler(address, *args):
    global world_min
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        world_mix = height

def eyeheight_max_handler(address, *args):
    global world_max
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        world_max = height

def scaling_allowed_handler(address, *args):
    global world_scaling_allowed
    if args[0] == False:
        world_scaling_allowed = False
        print("Avatar scaling has been \033[0;31mdisabled\033[0m.")
    else:
        world_scaling_allowed = True
        print("Avatar scaling has been \033[0;32menabled\033[0m.")

def eyeheight_handler(address, *args):
    global current_eyeheight
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        if current_eyeheight != height and not scaling:
            print("New eye height: " + str(height) + " m")
        current_eyeheight = height

def scalefactor_handler(address, *args):
    global current_scale_factor
    scale_factor = args[0]
    if isinstance(scale_factor, int):
        scale_factor = float(height)
    if isinstance(scale_factor, float):
        current_scale_factor = scale_factor

def custom_scaling_handler(address, *args):
    # TODO: Add compatibility with custom scaling systems
    pass

def start_server(ip, port):
    global server
    if server:
        raise Exception("OSC server has already been started.")
    print(f"Starting OSC server on {ip}:{port}")
    dispatch = dispatcher.Dispatcher()
    dispatch.map("/avatar/eyeheightmin", eyeheight_min_handler)
    dispatch.map("/avatar/eyeheightmax", eyeheight_max_handler)
    dispatch.map("/avatar/eyeheightscalingallowed", scaling_allowed_handler)
    dispatch.map("/avatar/eyeheight", eyeheight_handler)
    dispatch.map("/avatar/parameters/ScaleFactor", scalefactor_handler)
    dispatch.map("/avatar/parameters/*", custom_scaling_handler)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatch)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print("Started OSC server.")

def start_client(ip, port):
    global client
    print(f"Starting OSC client on {ip}:{port}")
    client = SimpleUDPClient(ip, port)
    print("Started OSC client.")

def process_command(command):
    global world_min
    global world_max
    global world_scaling_allowed
    global scaling_duration
    height = current_eyeheight
    if command == "quit" or command == "exit":
        quit()
    elif command == "help":
        print("Available commands:")
        print(" quit | exit  : Quits the app.")
        print(" info | i     : Shows various information about your size and limits.")
        print(" min          : Sets your height to the minimum height set by the world.")
        print(" max          : Sets your height to the maximum height set by the world.")
        print(" override | o : Makes the app forget the world limitations.")
        print(" ")
        print("To change your size, just type your desired eye height (in meters).")
        print("Do NOT add unit suffixes! They are not supported, for now.")
    elif command == "min":
        height = world_min
    elif command == "max":
        height = world_max
    elif command == "info" or command == "i":
        if current_eyeheight > 0:
            print("Calculated base eye height: ", get_base_eyeheight(), 'm')
            print("Current eye height: ", current_eyeheight, 'm')
            print("Current scale factor: ", current_scale_factor)
        else:
            print("Scaling/height data not available. Please change your height first.")
        if world_scaling_allowed:
            if world_min == 0 and world_max == 0:
                print("World scaling limits are unknown.")
                print("Please (re)join a world or use the override command.")
            else:
                print("World min eye height: ", world_min, 'm')
                print("World max eye height: ", world_max, 'm')
                print("Note: You may be able to go over these limits.")
                print("      Only some worlds actually enforce them.")
        else:
            print("Avatar scaling is currently disabled.")
    elif command == "override" or command == "o":
        world_min = MIN_HEIGHT
        world_max = MAX_HEIGHT
        world_scaling_allowed = True
        scaling = False
        print("Forgot world limits ;)")
        print("You may encounter weird behavior.")
    elif command == "instant":
        scaling_duration = 0
    elif command == "smooth":
        scaling_duration = float(config["experimental.smoothScaling"]["LengthSeconds"])
    else:
        try:
            desired_height = float(command)
        except:
            print("Unknown command.")
        else:
            if desired_height < MIN_HEIGHT:
                print("too small")
            elif desired_height > MAX_HEIGHT:
                print("too big")
            else:
                if world_scaling_allowed:
                    set_eyeheight(desired_height)
                    return
                else:
                    print("Avatar scaling not available!")
    if height != current_eyeheight:
        if world_scaling_allowed:
            set_eyeheight(height)
        else:
            print("Avatar scaling not available!")

def set_eyeheight(height):
    global scaling
    height = min(max(height, MIN_HEIGHT), MAX_HEIGHT)
    if scaling:
        return
    if client:
        if scaling_duration > 0 and current_eyeheight != height:
            difference = height - current_eyeheight
            step_length = float(config["experimental.smoothScaling"]["StepLengthSeconds"])
            num_steps = scaling_duration / step_length
            scaling = True
            for h in float_range(current_eyeheight, height, difference / num_steps):
                client.send_message("/avatar/eyeheight", [h])
                time.sleep(step_length)
            time.sleep(0.2)
            scaling = False
        client.send_message("/avatar/eyeheight", [height])
    else:
        raise Exception("set_eyeheight has been called without a client")

def main():
    print("\033[0;33m[ KutayX7's VRChat Avi Scaler ]\033[0m")
    print("For issues and feedback, visit https://github.com/KutayX7/vrc-avi-scaler/issues")
    print("Type \"quit\" to quit.")
    print("--------------------")
    start_server(DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT)
    start_client(DEFAULT_CLIENT_IP, DEFAULT_CLIENT_PORT)
    print("")
    while True:
        process_command(input(""))

if __name__ == "__main__":
    main()
