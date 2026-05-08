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
                target_eyeheight = current_eyeheight * value
                set_eyeheight(target_eyeheight)
                set_parameter("KtySize/ScaleRelative", 1.0)
            case "KtySize/ScaleIncrement" if (
                isinstance(value, float) and value != 0.0):
                target_eyeheight = current_eyeheight + value
                set_eyeheight(target_eyeheight)
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
