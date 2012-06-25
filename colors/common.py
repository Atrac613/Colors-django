# -*- coding: utf-8 -*-
import string
import math

from random import choice
from PIL import Image, ImageOps

def gen_imagekey(length=6, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

def gen_thumbnail(input_file, output_file):
    image = Image.open(input_file)
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    image.thumbnail((400, 400), Image.ANTIALIAS)
    image.save(output_file, 'JPEG', quality=90)

def get_colors(input_file, depth=50):
    image = Image.open(input_file)
    image = image.resize((3,3))
    colors = image.getcolors()
    
    colors = sorted(colors, key=lambda pair: pair[1], reverse=True)

    color_list = []
    ignore_color_list = []

    for color in colors:
        rgb = color[1]

        if rgb in ignore_color_list:
            continue

        for color_tmp in colors:
            rgb_tmp = color_tmp[1]

            r = rgb[0] - rgb_tmp[0]
            g = rgb[1] - rgb_tmp[1]
            b = rgb[2] - rgb_tmp[2]

            if depth > math.sqrt(r * r + g * g + b * b):
                if rgb not in color_list:
                    color_list.append(rgb)

                ignore_color_list.append(rgb_tmp)

    return color_list

def get_colors_recursive(image_file, list_length=4):
    colors = []

    for depth in reversed(range(0, 100)):
        colors = get_colors(image_file, depth)
        if len(colors) >= 4:
            break;

    return colors

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

