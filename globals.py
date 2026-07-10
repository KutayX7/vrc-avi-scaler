
# Check out the `config` command to find the real configuration file.

# PLEASE DON'T MODIFY THIS FILE
# UNLESS YOU KNOW WHAT YOU'RE DOING!
# Please don't make a bug report if you modified this file.

from translator import Translator
from simple_types import Any, Height, ScaleFactor, ParameterValue, TrackingType

# General
FPS: float = 90.0
save_config_on_exit: bool = False

# OSC
osc_client_ip: str = "127.0.0.1"
osc_client_port: int = 9000
osc_server_ip: str = "127.0.0.1"
osc_server_port: int = 9001
osc_debug_log: bool = False

# Compatibility with third-party scaling systems
compat_mags: bool = True # Mag's Scale Adjuster
compat_jackal: bool = True # Jackal Scaling System
compat_openvrcs: bool = True # OpenVRCScaler

# VRChat avatar eye-height limits (in meters)
MIN_EYEHEIGHT: Height =     0.01
MAX_EYEHEIGHT: Height = 10000.0

# Locale
preferred_locale: str = "auto"
preferred_unit_of_length: str = "metres"

# Internal (PLEASE DO NOT TOUCH)
config: Any = None
server: Any = None
client: Any = None
current_eyeheight: Height = 0.0
current_scale_factor: ScaleFactor = 0.0
world_min_eyeheight: Height = 0.0
world_max_eyeheight: Height = 0.0
world_scaling_allowed: bool = True
scaling: bool = False
scaling_id: int = 0
target_eyeheight: Height = 0
smooth_scaling_step_frequency: float = 1.0
smooth_scaling_duration: float = 0.0
smooth_scaling_default_duration: float = 3.0
tracking_type: TrackingType = 0
VRMode: bool = False
compat_killswitch: bool = False
avatar_parameters: dict[str, ParameterValue] = {}
oscquery_enabled: bool = True
oscquery_service_ip: str = "127.0.0.1"
oscquery_service_port: int = 9070
oscquery_vrchat_service_name: str = ""
oscquery_vrchat_address: str = ""
oscquery_vrchat_port: int = 9000
oscquery_listener: Any = None
oscquery_service: Any = None
oscquery_http_server: Any = None
osc_detected_VRChat_ip: str = ""
auto_apply_client_fix: bool = False
vrmode_lock: bool = False
translator: Any = None
commands: set[Any] = set() # to be replaced at runtime
