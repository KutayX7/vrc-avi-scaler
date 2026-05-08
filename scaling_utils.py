import globals

# returns the eyeheight when scale = 1
def get_base_eyeheight():
    current_scale_factor = globals.current_scale_factor
    if current_scale_factor == 0:
        return 0
    return globals.current_eyeheight / current_scale_factor

def scale_to_eyeheight(scale):
    return get_base_eyeheight() * scale

def eyeheight_to_scale(eyeheight):
    return eyeheight / get_base_eyeheight()
