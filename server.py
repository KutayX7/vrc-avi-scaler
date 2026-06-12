import threading
from pythonosc import dispatcher
from pythonosc import osc_server
import globals
import compat
from simple_types import Any, Callback

class Server:
    def __init__(self, ip: str, port: int):
        dispatch = dispatcher.Dispatcher()
        dispatch.map("*", self._filter, needs_reply_address=True)
        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatch)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self._dispatch = dispatch
        self._server = server
        self._thread = thread

    def _filter(self, client_address: str, address: str, *args: Any) -> None:
        ip = client_address[0]
        if ip != globals.osc_detected_VRChat_ip:
            globals.osc_detected_VRChat_ip = ip
            if globals.auto_apply_client_fix:
                client = globals.client
                if client:
                    globals.auto_apply_client_fix = False
                    client.reconnect(ip, client.port)

    def map(self, address: str, callback: Callback) -> None:
        self._dispatch.map(address, callback)

def set_vrmode(vrmode: bool, force: bool = False) -> None:
    if globals.vrmode_lock and not force:
        return
    if vrmode:
        if not globals.VRMode:
            print("Switched to VR mode.")
        globals.VRMode = True
    else:
        if globals.VRMode:
            print("Switched to non-VR mode.")
        globals.VRMode = False

def avatar_change_handler(address: str, *args: tuple[Any]) -> None:
    set_vrmode(False)
    print("Avatar has been changed.")
    if globals.current_scale_factor <= 0:
        globals.client.refresh_eyeheight()

def eyeheight_min_handler(address: str, *args: tuple[Any]) -> None:
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        globals.world_min_eyeheight = height

def eyeheight_max_handler(address: str, *args: tuple[Any]) -> None:
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float):
        globals.world_max_eyeheight = height

def scaling_allowed_handler(address: str, *args: tuple[Any]) -> None:
    world_scaling_allowed = args[0]
    if isinstance(world_scaling_allowed, bool):
        if world_scaling_allowed:
            if not globals.world_scaling_allowed:
                print("Avatar scaling has been \033[0;32menabled\033[0m.")
        else:
            if globals.world_scaling_allowed:
                print("Avatar scaling has been \033[0;31mdisabled\033[0m.")
        globals.world_scaling_allowed = world_scaling_allowed

def eyeheight_handler(address: str, *args: tuple[Any]) -> None:
    height = args[0]
    if isinstance(height, int):
        height = float(height)
    if isinstance(height, float) and height > 0.0:
        if (globals.current_eyeheight != height and
            (height == globals.target_eyeheight or (not globals.scaling))):
            print("New eye height: " + str(height) + " m")
        globals.current_eyeheight = height

def scalefactor_handler(address: str, *args: tuple[Any]) -> None:
    scale_factor: Any = args[0]
    if isinstance(scale_factor, int):
        scale_factor = float(scale_factor)
    if isinstance(scale_factor, float):
        globals.current_scale_factor = scale_factor

def vrmode_handler(address: str, *args: tuple[Any]) -> None:
    set_vrmode(not not args[0])

def trackingtype_handler(address: str, *args: tuple[Any]) -> None:
    trackingtype: Any = args[0]
    if isinstance(trackingtype, int):
        if trackingtype > 3:
            set_vrmode(True)
        globals.tracking_type = trackingtype

def custom_scaling_handler(address: str, *args: tuple[Any]) -> None:
    value = args[0]
    if isinstance(value, (bool, int, float)):
        compat.on_avatar_parameter_change(address[19:], value)

def osc_debug_handler(address: str, *args: tuple[Any]) -> None:
    if globals.osc_debug_log:
        print(f"[DEBUG] OSC: {address} {args}")

def start_server(ip: str, port: int) -> Server:
    server = Server(ip, port)
    server.map("/*", osc_debug_handler)
    server.map("/avatar/change", avatar_change_handler)
    server.map("/avatar/eyeheightmin", eyeheight_min_handler)
    server.map("/avatar/eyeheightmax", eyeheight_max_handler)
    server.map("/avatar/eyeheightscalingallowed", scaling_allowed_handler)
    server.map("/avatar/eyeheight", eyeheight_handler)
    server.map("/avatar/parameters/ScaleFactor", scalefactor_handler)
    server.map("/avatar/parameters/TrackingType", trackingtype_handler)
    server.map("/avatar/parameters/VRMode", vrmode_handler)
    server.map("/avatar/parameters/*", custom_scaling_handler)
    print(f"Started OSC server on {ip}:{port}")
    return server
