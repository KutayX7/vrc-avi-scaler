from time import sleep
from threading import Timer
from pythonosc.udp_client import SimpleUDPClient
import globals
from scaling_utils import quantize_height, clamp_eyeheight
from simple_types import Height, ParameterValue, Any
from translator import printl

class Client:
    def __init__(self, ip: str, port: int):
        self._client = SimpleUDPClient(ip, port)
        self.ip = ip
        self.port = port
        globals.scaling = False

    def reconnect(self, ip: str, port: int) -> None:
        self._client = SimpleUDPClient(ip, port)
        self.ip = ip
        self.port = port
        printl("client.address_changed", address=f"{ip}:{port}")

    def send_message(self, address: str, value: Any) -> None:
        self._client.send_message(address, value)

    def set_parameter(self, parameter: str, value: ParameterValue) -> None:
        self.send_message("/avatar/parameters/" + parameter, [value])

    def _set_eyeheight_instantly(self, eyeheight: Height, adjust:bool = False, scaling_id:int = 0) -> None:
        if scaling_id != 0:
            if globals.scaling_id != scaling_id:
                return
        if adjust:
            current_eyeheight = globals.current_eyeheight
            quantized_height = quantize_height(eyeheight)
            if quantized_height == quantize_height(current_eyeheight):
                eyeheight += 0.00125
        self.send_message("/avatar/eyeheight", [float(eyeheight)])

    def refresh_eyeheight(self, delay: float = 1.0) -> None:
        sleep(delay)
        current_eyeheight = globals.current_eyeheight
        if current_eyeheight <= 0:
            return
        if globals.current_scale_factor > 0:
            return
        printl("client.auto_height_check.begin")
        temp_eyeheight = current_eyeheight - 0.0015
        if current_eyeheight < 1:
            temp_eyeheight += 0.003
        self._set_eyeheight_instantly(temp_eyeheight)
        sleep(0.1)
        self._set_eyeheight_instantly(current_eyeheight)
        sleep(0.2)
        printl("client.auto_height_check.complete")
        if globals.current_scale_factor > 0:
            printl("client.auto_height_check.result.success")
        else:
            printl("client.auto_height_check.result.fail")
            delay += 1.0
            printl("client.auto_height_check.retry", time=delay)
            self.refresh_eyeheight(delay)

    def set_eyeheight(self, target_eyeheight: Height, duration: float = 0.0) -> None:
        target_eyeheight = clamp_eyeheight(target_eyeheight)
        globals.target_eyeheight = target_eyeheight
        scaling_id = globals.scaling_id + 1
        globals.scaling_id = scaling_id
        if duration > 0.0 and globals.current_eyeheight != target_eyeheight:
            globals.scaling = True
            height = clamp_eyeheight(globals.current_eyeheight)
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
            sleep(duration + 0.25)
        self._set_eyeheight_instantly(target_eyeheight, scaling_id=scaling_id)
        if globals.scaling_id == scaling_id:
            globals.scaling = False

def start_client(ip: str, port: int) -> Client:
    client = Client(ip, port)
    printl("client.started", address=f"{ip}:{port}")
    return client
