import math
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

def parse_to_meters(text, default, print=print):
    number = ""
    unit = ""
    for char in text:
        if char in "0123456789.":
            number += char
        elif not (char in " \n\r\t"):
            unit += char
    if len(number) < 1:
        raise Exception("Not a number.")
    if number.endswith('.'):
        number = number[:-1]
    height = float(number)
    unit = unit.lower()
    match unit:
        case '':
            pass
        case 'meters' | 'metres' | 'meter' | 'metre' | 'm':
            pass
        case 'decimeters' | 'decimetres' | 'decimeter' | 'decimetre' | 'dm':
            height *= 0.1
        case 'centimeters' | 'centimetres' | 'centimeter' | 'centimetre' | 'cm':
            height *= 0.01
        case 'millimeters' | 'millimetres' | 'millimeter' | 'millimetre' | 'mm':
            height *= 0.001
        case 'kilometers' | 'kilometres' | 'kilometer' | 'kilometre' | 'km':
            height *= 1000.0
        case 'feet' | 'foot' | 'ft':
            height *= 0.3048
        case 'miles' | 'mile' | 'mil' | 'mi':
            height *= 1609.34
        case 'inches' | 'inch' | 'in':
            height *= 0.0254
        case 'yards' | 'yard' | 'yd':
            height *= 0.9144
        case _:
            print(f"Unknown length unit: {unit}")
            height = default
    return height

def quantize_height(height):
    height = float(height)
    return str(math.floor(height*2000)/2000)
