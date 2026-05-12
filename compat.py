import time
import globals
import scaling_utils

parameters = {}

debounce = False

def set_eyeheight(height, instant=False):
    if instant:
        globals.client.set_eyeheight(height, 0)
    else:
        globals.client.set_eyeheight(height, globals.smooth_scaling_duration)

def set_parameter(parameter, value):
    globals.client.set_parameter(parameter, value)

def scale_by_factor(factor, instant=False):
    set_eyeheight(globals.current_eyeheight * factor, instant)

def scale_by_increment(increment, instant=False):
    set_eyeheight(globals.current_eyeheight + increment, instant)

def on_avatar_parameter_change(parameter, value):
    global debounce
    parameters[parameter] = value

    if debounce:
        return

    if (parameter.startswith("KtySize") and
        parameters.get("KtySize/Enabled", True)):
        # This is for my own OSC scaling system.
        # If you're a scaling system creator,
        # feel free to add compatibility. :)
        # All parameters mentioned here are animator only,
        # don't add these to avatar parameters!
        # Use other parameters to drive these.
        # NOT STABLE YET!
        current_eyeheight = globals.current_eyeheight
        current_scale = globals.current_scale_factor
        match parameter:
            case "KtySize/Duration" if isinstance(value, float):
                globals.smooth_scaling_duration = value
            case "KtySize/Frequency" if isinstance(value, float) and value > 1:
                globals.smooth_scaling_step_frequency = value
            case "KtySize/SetEyeheight" if value:
                target_eyeheight = float(
                    parameters.get("KtySize/TargetEyeheight", current_eyeheight))
                set_eyeheight(target_eyeheight)
                set_parameter("KtySize/SetEyeheight", False)
            case "KtySize/SetScale" if value:
                target_scale = float(
                    parameters.get("KtySize/TargetScale", current_scale))
                target_eyeheight = scaling_utils.scale_to_eyeheight(target_scale)
                set_eyeheight(target_eyeheight)
                set_parameter("KtySize/SetScale", False)
            case "KtySize/ScaleRelative" if (
                isinstance(value, float) and value != 1.0 and value > 0):
                scale_by_factor(value)
                set_parameter("KtySize/ScaleRelative", 1.0)
            case "KtySize/ScaleIncrement" if (
                isinstance(value, float) and value != 0.0):
                scale_by_increment(value)
                set_parameter("KtySize/ScaleIncrement", 0.0)
            case "KtySize/Reset" if value:
                set_eyeheight(scaling_utils.get_base_eyeheight())
                set_parameter("KtySize/Reset", False)
            case _:
                pass

    # Mag's Scale Adjuster compatibilty
    # As you can imagine, it was pain to get it to work... I mean... barely work.
    if globals.compat_magsscaleadjuster:
        if parameter == "ScaleOverlay" and value:
            # Disables incremental scaling, which I couldn't get to work reliably
            set_parameter("ScaleOverlay", False)
        current_scale = parameters.get("CurrentScale", 73)
        if (parameter == "NextScale" and
            (parameters.get("ReadyReset", False) or
            parameters.get("NoReadyReset", False)) and
            value > 0 and value != current_scale):
            debounce = True
            target_scale = 0.01 * (1.0651169 ** value)
            target_eyeheight = scaling_utils.scale_to_eyeheight(target_scale)
            set_eyeheight(target_eyeheight, current_scale != 73)
            set_parameter("CurrentScale", value)
            set_parameter("NextScale", value)
            time.sleep(0.2)
            set_parameter("NextScale", value)
            time.sleep(0.2)
            debounce = False
            # Yes, every lne is needed.

    # Jackal Scaling System compatibility
    # Works really well.
    if globals.compat_jackalscaling:
        match parameter:
            case "JackalOSCFineTune" if isinstance(value, int) and value > 0:
                factor = 1.0
                increment = 0.0
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
            case "JackalOSCScale" if (isinstance(value, int) and
                value >= 0 and value <= 38):
                heights = [
                    scaling_utils.get_base_eyeheight(),
                    0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8,
                    2.0, 2.5, 3.0, 4.0, 5.0,
                    7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0,
                    50.0, 75.0, 100.0, 150.0, 200.0, 300.0, 400.0,
                    500.0, 750.0, 1000.0, 1500.0, 2000.0, 3000.0,
                    4000.0, 5000.0, 6000.0, 8000.0, 10000.0
                    ]
                set_eyeheight(heights[value])
            case "JackalOSCScaleSpeed" if (isinstance(value, int) and
                value >= 0 and value <= 9):
                timings = [
                    0,
                    3, 5, 10, 30,
                    60, 120, 180, 300, 600
                    ]
                globals.smooth_scaling_duration = timings[value]
                scale_by_factor(1, True)
