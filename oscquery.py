import socket
import threading
import globals
import json
from urllib.request import urlopen
from zeroconf import IPVersion, ServiceInfo, ServiceBrowser, ServiceListener, Zeroconf
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

zeroconf = Zeroconf()

def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', 0))
        port: int = 0
        _, port = sock.getsockname()
        return port

def get_ip_address() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip: str = "127.0.0.1"
    try:
        sock.connect(('1.1.1.1', 1))
        ip, _ = sock.getsockname()
    except:
        pass
    finally:
        sock.close()
    return ip

class OSCQueryHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path

        NAME = "KutayX7's VRChat Avi Scaler"

        HOST_INFO = {
            "NAME": NAME,
            "EXTENSIONS": {
                "ACCESS": True,
                "CLIPMODE": False,
                "RANGE": True,
                "TYPE": True,
                "VALUE": True
            },
            "OSC_IP": globals.oscquery_service_ip,
            "OSC_PORT": globals.oscquery_service_port,
            "OSC_TRANSPORT": "UDP"
        }

        ROOT = {
            "NAME": NAME,
            "FULL_PATH": "/",
            "DESCRIPTION": "KutayX7's avatar scaling system",
            "CONTENTS": {
                "avatar": {
                    "FULL_PATH": "/avatar",
                    "CONTENTS": {
                        "change": {
                            "FULL_PATH": "/avatar/change",
                            "TYPE": "s"
                        }
                    }
                }
            }
        }

        response_json = ""

        code = 200

        match path:
            case "/":
                response_json = json.dumps(ROOT)
            case "/?HOST_INFO":
                response_json = json.dumps(HOST_INFO)
            case _:
                code = 404
                response_json = json.dumps({})

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response_json.encode("utf-8"))

    # disable http server logs
    def log_message(self, format: Any, *args: Any) -> None:
        pass

def _is_local(address: str) -> bool:
    match address:
        case "localhost":
            return True
        case "127.0.0.1":
            return True
        case "127.0.1.1":
            return True
        case "10.10.10.10":
            return True
        case "::1":
            return True
    return False

def _select_prefer_non_local(*addresses: str) -> str:
    preferred: str = addresses[0]
    for address in addresses:
        if not _is_local(address):
            preferred = address
    return preferred

class OSCQueryListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        if name == globals.oscquery_vrchat_service_name:
            globals.oscquery_vrchat_service_name = ""
            print("VRChat OSCQuery service has been removed.")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info and name.startswith("VRChat-Client-"):
            address: str = socket.inet_ntoa(info.addresses[0])
            assert isinstance(info.port, int)
            port: int = info.port
            print(f"Detected VRChat OSCQuery service at {address}:{port}")
            globals.oscquery_vrchat_service_name = name
            globals.oscquery_vrchat_address = address
            globals.oscquery_vrchat_port = port
            client = globals.client
            if client:
                osc_address = get_VRChat_OSC_address()
                if osc_address:
                    client.reconnect(*osc_address)
                else:
                    address = _select_prefer_non_local(
                        address, globals.osc_client_ip
                    )
                    if _is_local(address):
                        globals.auto_apply_client_fix = True
                    client.reconnect(address, client.port)

def start_listener() -> None:
    oscquery_listener = OSCQueryListener()
    browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", oscquery_listener)
    globals.oscquery_listener = oscquery_listener

def _run_async(target: Any, *args: Any) -> Any:
    thread = threading.Thread(target=target, args=args)
    thread.daemon = True
    thread.start()

def _start_http_server(port: int) -> None:
    http_server = HTTPServer(('', port), OSCQueryHandler)
    _run_async(target=http_server.serve_forever)
    globals.oscquery_http_server = http_server

def _start_service(ip: str, port: int) -> None:
    properties = {}
    properties[b'txtvers'] = b'1'
    oscquery_service = ServiceInfo(
        "_oscjson._tcp.local.",
        "KutayX7_VRChat_Avi_Scaler._oscjson._tcp.local.",
        addresses=[socket.inet_aton(ip)],
        port=port,
        server="KutayX7_VRChat_Avi_Scaler._oscjson.local.",
        properties=properties,
    )
    zeroconf.register_service(oscquery_service)
    globals.oscquery_service = oscquery_service

def start_service() -> None:
    service_ip = get_ip_address()
    service_port = get_free_port()
    globals.oscquery_service_ip = service_ip
    globals.oscquery_service_port = service_port
    print(f"Starting OSCQuery service at {service_ip}:{service_port}")
    _run_async(_start_service, service_ip, service_port)
    _run_async(_start_http_server, service_port)

def is_vrchat_running() -> bool:
    return not not globals.oscquery_vrchat_service_name

def get_VRChat_OSC_address() -> tuple[str, int] | None:
    if not is_vrchat_running():
        return None
    ip = globals.oscquery_vrchat_address
    port = globals.oscquery_vrchat_port
    try:
        with urlopen(f"http://{ip}:{port}/?HOST_INFO") as f:
            data = json.loads(f.read().decode('utf-8'))
            return (data["OSC_IP"], data["OSC_PORT"])
    except Exception as e:
        print("Failed to get OSC info from VRChat.", e)
        return None

def get_value(address: str) -> tuple[Any, bool]:
    if not is_vrchat_running():
        return (None, False)
    ip = globals.oscquery_vrchat_address
    port = globals.oscquery_vrchat_port
    try:
        with urlopen(f"http://{ip}:{port}{address}") as f:
            data = json.loads(f.read().decode('utf-8'))
            return (data["VALUE"][0], True)
    except Exception as e:
        return (None, False)

