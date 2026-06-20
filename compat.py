from time import sleep
import globals
from scaling_utils import scale_to_eyeheight, get_base_eyeheight, is_valid_float
from simple_types import Any, Height, ScaleFactor, ParameterValue

debounce: bool = False

def set_eyeheight(height: float, instant: bool = False) -> None:
    if instant:
        globals.client.set_eyeheight(height, 0)
    else:
        globals.client.set_eyeheight(height, globals.smooth_scaling_duration)

def get_parameter(parameter: str) -> ParameterValue | None:
    return globals.avatar_parameters.get(parameter)

def set_parameter(parameter: str, value: ParameterValue) -> None:
    globals.avatar_parameters[parameter] = value
    globals.client.set_parameter(parameter, value)

def get_bool(parameter: str, default: bool = False) -> bool:
    value = get_parameter(parameter)
    if type(value) is bool:
        return value
    else:
        return default

def get_int(parameter: str, default: int = 0) -> int:
    value = get_parameter(parameter)
    if type(value) is int:
        return value
    return default

def get_float(parameter: str, default: float = 0.0) -> float:
    value = get_parameter(parameter)
    if type(value) is float:
        return value
    return default

def scale_by_factor(factor: float, instant: bool = False) -> None:
    set_eyeheight(globals.current_eyeheight * factor, instant)

def scale_by_increment(increment: float, instant: bool = False) -> None:
    set_eyeheight(globals.current_eyeheight + increment, instant)

def handle_ktysize(parameter: str, value: ParameterValue) -> None:
    # This is for my own OSC scaling system.
    # If you're a scaling system creator,
    # feel free to add compatibility. :)
    # ALL FLOAT parameters mentioned here are ANIMATOR ONLY,
    # don't add them to VRChat avatar parameters!
    # Use other parameters to drive them.
    prefix: str = "KtySize/"
    match parameter[len(prefix):]:
        case "Duration" if isinstance(value, float):
            globals.smooth_scaling_duration = abs(value)
        case "Frequency" if isinstance(value, float) and value > 1:
            globals.smooth_scaling_step_frequency = abs(value)
        case _:
            pass
    if not get_bool(f"{prefix}Enabled", True):
        return
    match parameter[len(prefix):]:
        case "SetEyeheight" if isinstance(value, bool) and value:
            target_eyeheight = get_float(
                f"{prefix}TargetEyeheight",
                globals.current_eyeheight
            )
            set_eyeheight(target_eyeheight)
            set_parameter(f"{prefix}SetEyeheight", False)
        case "SetEyeheight" if isinstance(value, float) and value > 0:
            set_eyeheight(value)
            set_parameter(f"{prefix}SetEyeheight", 0.0)
        case "SetScale" if isinstance(value, bool) and value:
            target_scale = get_float(
                f"{prefix}TargetScale",
                globals.current_scale_factor
            )
            target_eyeheight = scale_to_eyeheight(target_scale)
            set_eyeheight(target_eyeheight)
            set_parameter(f"{prefix}SetScale", False)
        case "SetScale" if isinstance(value, float) and value > 0:
            target_eyeheight = scale_to_eyeheight(value)
            set_eyeheight(target_eyeheight)
            set_parameter(f"{prefix}SetScale", 0.0)
        case "ScaleRelative" if (
            isinstance(value, float) and value != 1.0 and value > 0):
            scale_by_factor(value)
            set_parameter(f"{prefix}ScaleRelative", 1.0)
        case "ScaleIncrement" if (
            isinstance(value, float) and value != 0.0):
            scale_by_increment(value)
            set_parameter(f"{prefix}ScaleIncrement", 0.0)
        case "Reset" if (
            isinstance(value, bool) and value):
            set_eyeheight(get_base_eyeheight())
            set_parameter(f"{prefix}Reset", False)
        case _:
            pass

def handle_mags(parameter: str, value: ParameterValue) -> None:
    # Mag's Scale Adjuster compatibilty
    global debounce
    current_scale: int = get_int("CurrentScale", 73)
    match parameter:
        case "ScaleOverlay" if not not value:
            # Disables incremental scaling, which I couldn't get to work reliably
            set_parameter("ScaleOverlay", False)
        case "NextScale" if (isinstance(value, int) and
                (get_bool("ReadyReset") or get_bool("NoReadyReset")) and
                value > 0 and value != current_scale):
            debounce = True
            target_scale: float = 0.01 * (1.0651169 ** value)
            target_eyeheight: float = scale_to_eyeheight(target_scale)
            set_eyeheight(target_eyeheight, current_scale != 73)
            set_parameter("CurrentScale", value)
            set_parameter("NextScale", value)
            sleep(0.2)
            set_parameter("NextScale", value)
            sleep(0.2)
            debounce = False
        case _:
            pass

def handle_jackal(parameter: str, value: ParameterValue) -> None:
    # Jackal Scaling System compatibility
    prefix: str = "JackalOSC"
    match parameter[len(prefix):]:
        case "FineTune" if isinstance(value, int) and value > 0:
            factor: float = 1.0
            increment: float = 0.0
            match value:
                case 1:
                    factor = 2.0
                case 2:
                    factor = 0.5
                case 3:
                    increment = 0.01
                case 4:
                    increment = 0.05
                case 5:
                    increment = 0.25
                case 6:
                    increment = 1.0
                case 7:
                    increment = 5.0
                case 8:
                    increment = 25.0
                case 9:
                    increment = -0.01
                case 10:
                    increment = -0.05
                case 11:
                    increment = -0.25
                case 12:
                    increment = -1.0
                case 13:
                    increment = -5.0
                case 14:
                    increment = -25.0
            if factor != 1.0:
                scale_by_factor(factor)
            if increment != 0.0:
                scale_by_increment(increment)
        case "Scale" if (isinstance(value, int) and
            value >= 0 and value <= 38):
            heights: list[float] = [
                get_base_eyeheight(),
                0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8,
                2.0, 2.5, 3.0, 4.0, 5.0,
                7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0,
                50.0, 75.0, 100.0, 150.0, 200.0, 300.0, 400.0,
                500.0, 750.0, 1000.0, 1500.0, 2000.0, 3000.0,
                4000.0, 5000.0, 6000.0, 8000.0, 10000.0
            ]
            set_eyeheight(heights[value])
        case "ScaleSpeed" if (isinstance(value, int) and
            value >= 0 and value <= 9):
            timings: list[float] = [
                0.0,
                3.0, 5.0, 10.0, 30.0,
                60.0, 120.0, 180.0, 300.0, 600.0
            ]
            globals.smooth_scaling_duration = timings[value]
        case _:
            pass

def handle_openvrcs(parameter: str, value: ParameterValue) -> None:
    # OpenVRCScaler compatibility
    prefix: str = "OpenVRCScaler_"
    match parameter[len(prefix):]:
        case "TransitionTime" | "TransistionTime" if (isinstance(value, float) and
            value >= 0.0 and value <= 1.0):
            globals.smooth_scaling_duration = value * 100.0
        case _:
            pass
    if not get_bool(f"{prefix}ScalingEnabled", False):
        return
    match parameter[len(prefix):]:
        case "ScalingEnabled" | "Decimal" | "Ones" | "Hundreds":
            target_eyeheight = (
                get_float(f"{prefix}Decimal") * 1.0 +
                get_float(f"{prefix}Ones") * 100.0 +
                get_float(f"{prefix}Hundreds") * 10000.0
            )
            set_eyeheight(target_eyeheight)
        case _:
            pass

def on_avatar_parameter_change(parameter: str, value: ParameterValue) -> None:
    if (globals.compat_killswitch or
            (isinstance(value, float) and
            not is_valid_float(value))):
        return

    globals.avatar_parameters[parameter] = value

    if debounce:
        return

    if parameter.startswith("KtySize/"):
        handle_ktysize(parameter, value)

    if globals.compat_mags:
        handle_mags(parameter, value)

    if globals.compat_jackal:
        handle_jackal(parameter, value)

    if globals.compat_openvrcs:
        handle_openvrcs(parameter, value)
