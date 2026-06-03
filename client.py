import time
from threading import Timer
from pythonosc.udp_client import SimpleUDPClient
import globals
from scaling_utils import quantize_height

class Client:
    def __init__(self, ip, port):
        self._client = SimpleUDPClient(ip, port)
        globals.scaling = False

    def send_message(self, address, value):
        self._client.send_message(address, value)

    def set_parameter(self, parameter, value):
        self.send_message("/avatar/parameters/" + parameter, [value])

    def _set_eyeheight_instantly(self, eyeheight, adjust=False, scaling_id=0):
        if scaling_id != 0:
            if globals.scaling_id != scaling_id:
                return
        if adjust:
            current_eyeheight = globals.current_eyeheight
            quantized_height = quantize_height(eyeheight)
            if quantized_height == quantize_height(current_eyeheight):
                eyeheight += 0.00125
        self.send_message("/avatar/eyeheight", [float(eyeheight)])

    def refresh_eyeheight(self, delay=1):
        time.sleep(delay)
        current_eyeheight = globals.current_eyeheight
        if current_eyeheight <= 0:
            return
        if globals.current_scale_factor > 0:
            return
        print("Doing an automatic avatar height check...")
        temp_eyeheight = current_eyeheight - 0.0015
        if current_eyeheight < 1:
            temp_eyeheight += 0.003
        self._set_eyeheight_instantly(temp_eyeheight)
        time.sleep(0.1)
        self._set_eyeheight_instantly(current_eyeheight)
        time.sleep(0.2)
        print("Height check complete.")
        if globals.current_scale_factor > 0:
            print("Result: SUCCESS")
        else:
            print("Result: FAIL")
            delay += 1
            print(f"Retrying in {delay} seconds...")
            self.refresh_eyeheight(delay)

    def set_eyeheight(self, target_eyeheight, duration=0):
        target_eyeheight = min(max(target_eyeheight, globals.MIN_HEIGHT), globals.MAX_HEIGHT)
        globals.target_eyeheight = target_eyeheight
        scaling_id = globals.scaling_id + 1
        globals.scaling_id = scaling_id
        if duration > 0 and globals.current_eyeheight != target_eyeheight:
            globals.scaling = True
            height = max(globals.current_eyeheight, globals.MIN_HEIGHT)
            step_length = 1 / globals.smooth_scaling_step_frequency
            num_steps = duration / step_length
            geometric_difference = target_eyeheight / height
            scale_per_step = geometric_difference ** (1/num_steps)
            adjust = not globals.VRMode
            for i in range(int(num_steps)):
                height *= scale_per_step
                timer = Timer(
                    i * step_length,
                    self._set_eyeheight_instantly,
                    args=[height],
                    kwargs={"adjust": adjust, "scaling_id": scaling_id}
                    )
                timer.daemon = True
                timer.start()
            time.sleep(duration + 0.25)
        self._set_eyeheight_instantly(target_eyeheight, scaling_id=scaling_id)
        if globals.scaling_id == scaling_id:
            globals.scaling = False

def start_client(ip, port):
    client = Client(ip, port)
    print(f"Started OSC client on {ip}:{port}")
    return client
