
FPS = 60.0 # Set this to your in-gamne FPS cap.
VRMode = False # Set this to True if you only play in VR

# OSC
osc_client_ip = "127.0.0.1"
osc_client_port = 9000
osc_server_ip = "127.0.0.1"
osc_server_port = 9001

# Compatibility with 3rd-party scalers
compat_magsscaleadjuster = True # Mag's Scale Adjuster
compat_jackalscaling = True # Jackal Scaling System

# VRChat height limits
MIN_HEIGHT = 0.01
MAX_HEIGHT = 10000.0

# Don't touch anything below!
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
smooth_scaling_step_frequency = FPS * 4
smooth_scaling_duration = 0
smooth_scaling_jitter_range = 0.002
