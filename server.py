import threading
from pythonosc import dispatcher
from pythonosc import osc_server
import globals
import compat

class Server:
    def __init__(self, ip, port):
        dispatch = dispatcher.Dispatcher()
        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatch)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self._dispatch = dispatch
        self._server = server
        self._thread = thread

    def map(self, address, callback):
        self._dispatch.map(address, callback)

def eyeheight_min_handler(address, *args):
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        globals.world_min_eyeheight = height

def eyeheight_max_handler(address, *args):
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        globals.world_max_eyeheight = height

def scaling_allowed_handler(address, *args):
    if args[0] == False:
        globals.world_scaling_allowed = False
        print("Avatar scaling has been \033[0;31mdisabled\033[0m.")
    else:
        globals.world_scaling_allowed = True
        print("Avatar scaling has been \033[0;32menabled\033[0m.")

def eyeheight_handler(address, *args):
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        if (globals.current_eyeheight != height and
            (height == globals.target_eyeheight or (not globals.scaling))):
            print("New eye height: " + str(height) + " m")
        globals.current_eyeheight = height

def scalefactor_handler(address, *args):
    scale_factor = args[0]
    if isinstance(scale_factor, int):
        scale_factor = float(height)
    if isinstance(scale_factor, float):
        globals.current_scale_factor = scale_factor

def vrmode_handler(address, *args):
    vrmode = args[0]
    if isinstance(vrmode, int):
        if vrmode == 1:
            if not globals.VRMode:
                print("VR mode has been activated.")
            globals.VRMode = True
            globals.smooth_scaling_jitter_range = 0.0
        elif vrmode == 0:
            globals.VRMode = False

def custom_scaling_handler(address, *args):
    compat.on_avatar_parameter_change(address[19:], args[0])

def start_server(ip, port):
    server = Server(ip, port)
    server.map("/avatar/eyeheightmin", eyeheight_min_handler)
    server.map("/avatar/eyeheightmax", eyeheight_max_handler)
    server.map("/avatar/eyeheightscalingallowed", scaling_allowed_handler)
    server.map("/avatar/eyeheight", eyeheight_handler)
    server.map("/avatar/parameters/ScaleFactor", scalefactor_handler)
    server.map("/avatar/parameters/VRMode", vrmode_handler)
    server.map("/avatar/parameters/*", custom_scaling_handler)
    print(f"Started OSC server on {ip}:{port}")
    return server
