import os
import tomllib
from pathlib import Path
from enum import Enum
import globals

CONFIG_FILE_PATH = Path('.') / 'data' / 'config.toml'

class ConfigReadResult(Enum):
    SUCCESS = 0
    NOT_FOUND = 1
    ACCESS_DENIED = 2
    CORRUPTED = 3

def reset_config_file() -> None:
    newline = '\n'
    if os.name == "nt":
        newline = '\r\n'
    template = newline.join([
        f"# KutayX7's Avi Scaler main configuration file",
        f"",
        f"# General",
        f"fps = {float(globals.FPS)}",
        f"autosave = {str(globals.save_config_on_exit).lower()}",
        f"",
        f"# OSC settings",
        f"[osc.client]",
        f"ip   = '{globals.osc_client_ip}'",
        f"port = {globals.osc_client_port}",
        f"[osc.server]",
        f"ip   = '{globals.osc_server_ip}'",
        f"port = {globals.osc_server_port}",
        f"[oscquery]",
        f"enabled   = {str(globals.oscquery_enabled).lower()}",
        f"",
        f"# Compatibility with third-party scaling systems",
        f"[compat]",
        f"\"Mag's Scale Adjuster\" = {str(globals.compat_mags).lower()}",
        f"\"Jackal Scaling System\" = {str(globals.compat_jackal).lower()}",
        f"\"OpenVRCScaler\" = {str(globals.compat_openvrcs).lower()}",
        f""
    ])

    if CONFIG_FILE_PATH.exists():
        with CONFIG_FILE_PATH.open('w') as f:
            f.write(template)
    else:
        CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE_PATH.open('x') as f:
            f.write(template)

def save_config() -> None:
    print("Saving config...")
    reset_config_file()
    print("Saved config.")

def read_config() -> ConfigReadResult:
    if not CONFIG_FILE_PATH.exists():
        return ConfigReadResult.NOT_FOUND
    with CONFIG_FILE_PATH.open('rb') as f:
        data = None
        try:
            data = tomllib.load(f)
        except:
            return ConfigReadResult.CORRUPTED

        globals.FPS = float(data.get("fps", globals.FPS))
        globals.smooth_scaling_step_frequency = globals.FPS * 4.0
        globals.save_config_on_exit = bool(data.get("autosave", globals.save_config_on_exit))

        osc = data.get("osc", dict())
        oscquery = data.get("oscquery", dict())
        client = osc.get("client", dict())
        server = osc.get("server", dict())
        globals.osc_client_ip = client.get("ip", globals.osc_client_ip)
        globals.osc_client_port = client.get("port", globals.osc_client_port)
        globals.osc_server_ip = server.get("ip", globals.osc_server_ip)
        globals.osc_server_port = server.get("port", globals.osc_server_port)
        globals.oscquery_enabled = oscquery.get("enabled", globals.oscquery_enabled)

        compat = data.get("compat", dict())
        globals.compat_mags = compat.get("Mag's Scale Adjuster", globals.compat_mags)
        globals.compat_jackal = compat.get("Jackal Scaling System", globals.compat_jackal)
        globals.compat_openvrcs = compat.get("OpenVRCScaler", globals.compat_openvrcs)

        return ConfigReadResult.SUCCESS
