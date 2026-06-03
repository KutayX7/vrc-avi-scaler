
# Check out `data/config.toml` for configuration.
# The program will prompt you to create it if
# it doesn't exist or overwrite it if it got corrupted.

# PLEASE DON'T MODIFY THIS FILE
# UNLESS YOU KNOW WHAT YOU'RE DOING!
# Don't report an issue if you modified this file.

# General
FPS = 90.0
save_config_on_exit = False

# OSC
osc_client_ip = "127.0.0.1"
osc_client_port = 9000
osc_server_ip = "127.0.0.1"
osc_server_port = 9001
osc_debug_log = False

# Compatibility with third-party scaling systems
compat_magsscaleadjuster = True # Mag's Scale Adjuster
compat_jackalscaling = True # Jackal Scaling System

# VRChat avatar eye-height limits (in meters)
MIN_HEIGHT =     0.01
MAX_HEIGHT = 10000.0

# Internal (PLEASE DO NOT TOUCH)
server = None
client = None
current_eyeheight = 0.0
current_scale_factor = 0.0
world_min_eyeheight = 0.0
world_max_eyeheight = 0.0
world_scaling_allowed = True
scaling = False
scaling_id = 0
target_eyeheight = 0
smooth_scaling_step_frequency = 1
smooth_scaling_duration = 0
TrackingType = 0
VRMode = False
compat_killswitch = False
avatar_parameters = {}
commands = []
