#!/usr/bin/env python
from collections import namedtuple

ColorInfo = namedtuple('ColorInfo',
                       'hex_value name red green blue hue saturation lightness')
Match = namedtuple('Match', 'hex_value name exact original')
RGB = namedtuple('RGB', 'red green blue')
HSL = namedtuple('HSL', 'hue saturation lightness')

class NameThatColor(object):
    def __init__(self, colorfile):
        import csv
        self.color_info = []
        reader = csv.reader(open(colorfile))
        for hex_val, name in reader:
            red, green, blue = self.rgb(hex_val)
            hue, saturation, lightness = self.hsl(hex_val)
            self.color_info.append(ColorInfo(hex_val, name,
                                             red, green, blue,
                                             hue, saturation, lightness))

    def name(self, color):
        color = color.upper()

        if not 3 < len(color) < 7:
            return Match("#000000", "Invalid Color", False, color)
        elif len(color) % 3 == 0:
            color = "#" + color
        elif len(color) == 4:
            color = ''.join(['#',
                             color[1], color[1],
                             color[2], color[2],
                             color[3], color[3]])

        red, green, blue = self.rgb(color)
        hue, saturation, lightness = self.hsl(color)

        ndf1 = 0
        ndf2 = 0
        ndf = 0
        the_color = False
        df = -1

        for info in self.color_info:
            if color[1:] == info.hex_value:
                return Match(info.hex_value, info.name, True, color)

            ndf1 = (((red - info.red) ** 2) +
                    ((green - info.green) ** 2) +
                    ((blue - info.blue) ** 2))
            ndf2 = (((hue - info.hue) ** 2) +
                    ((saturation - info.saturation) ** 2) +
                    ((lightness - info.lightness) ** 2))
            ndf = ndf1 + ndf2 * 2

            if not 0 < df < ndf:
                df = ndf
                the_color = info

        
        if not the_color:
            return Match("#000000", "Invalid Color", False, color)
        else:
            return Match(the_color.hex_value,
                         the_color.name,
                         False,
                         color)
                             
    def rgb(self, color):
        return RGB(int(color[1:3], 16),
                   int(color[3:5], 16),
                   int(color[5:7], 16))
    def hsl(self, color):
        red, green, blue = self.rgb(color)

        red /= 255.0
        green /= 255.0
        blue /= 255.0

        min_color = min(red, min(green, blue))
        max_color = max(red, max(green, blue))
        delta = max_color - min_color
        lightness = (min_color + max_color) / 2

        saturation = 0;
        sat_mod = ((2 * lightness) if lightness < 0.5 else (2 - 2 * lightness))
        
        if 0 < lightness < 1:
            saturation = (delta / sat_mod)
                  
        hue = 0

        if delta > 0:
            if max_color == red and max_color != green:
                hue += (green - blue) / delta
            if max_color == green and max_color != blue:
                hue += (2 + (blue - red) / delta)
            if max_color == blue and max_color != red:
                hue += (4 + (red - green) / delta)
            hue /= 6
            
        return HSL(int(hue * 255),
                   int(saturation * 255),
                   int(lightness * 255))

if __name__ == '__main__':
    import os, json, sys
    csv_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data', 'colors.csv')
    Namer = NameThatColor(csv_file)
    color = sys.argv[1]
    print json.dumps(Namer.name(color))
    
