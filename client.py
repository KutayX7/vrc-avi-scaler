import time
from threading import Timer
from pythonosc.udp_client import SimpleUDPClient
import globals

class Client:
    def __init__(self, ip, port):
        self._client = SimpleUDPClient(ip, port)
        self._parity = globals.smooth_scaling_jitter_range
        globals.scaling = False

    def send_message(self, address, value):
        self._client.send_message(address, value)

    def set_parameter(self, parameter, value):
        self.send_message("/avatar/parameters/" + parameter, [value])

    def _set_eyeheight_instantly(self, eyeheight, jitter=False):
        if jitter:
            eyeheight = eyeheight * (self._parity + 1) + self._parity
            self._parity = -self._parity
        self.send_message("/avatar/eyeheight", [eyeheight])

    def set_eyeheight(self, target_eyeheight, duration=0):
        if globals.scaling:
            return
        globals.target_eyeheight = target_eyeheight
        if duration > 0 and globals.current_eyeheight != target_eyeheight:
            globals.scaling = True
            height = max(globals.current_eyeheight, globals.MIN_HEIGHT)
            step_length = 1 / globals.smooth_scaling_step_frequency
            num_steps = duration / step_length
            geometric_difference = target_eyeheight / height
            scale_per_step = geometric_difference ** (1/num_steps)
            for i in range(int(num_steps)):
                height *= scale_per_step
                timer = Timer(
                    i * step_length,
                    self._set_eyeheight_instantly,
                    args=[height, True])
                timer.daemon = True
                timer.start()
            time.sleep(duration + 0.25)
            globals.scaling = False
        self._set_eyeheight_instantly(target_eyeheight)

def start_client(ip, port):
    client = Client(ip, port)
    print(f"Started OSC client on {ip}:{port}")
    return client
