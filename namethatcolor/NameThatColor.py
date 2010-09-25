#!/usr/bin/env python
"""
name_that_color.py -- find names for hex colors
Copyright (c) 2010, Jeremiah Dodds <jeremiah.dodds@gmail.com>

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the conditions in LICENSE.txt are met

Provides a utility for retrieving the closest known "human readable" name for a
color specified as a hex string. It does this by using an algorithm ported from
ntc.js ( http://chir.ag/projects/ntc ). 

There are 3 different sets of color definitions to choose from:
  Resene ( http://people.csail.mit.edu/jaffer/Color/resenecolours.txt )
  html4 ( http://www.w3.org/TR/css3-color/#html4 )
  css3 ( http://www.w3.org/TR/css3-color/#svg-color )

css3 is a superset of html4.

The user can also supply their own colorfile to use. It should be comma
separated hex,name pairs, and should include the leading #. Commas are allowed
in names.

Currently two output formats are supported -- json, and raw. 

Usage:

As a command-line utility:

$ namethatcolor aabbcc
{"hex_value": "#B0C4DE", "name": "lightsteelblue"}
$ namethatcolor --color-set resene aabbcc
{"hex_value": "#ADBED1", "name": "Casper"}

#same as above
$ namethatcolor -s resene aabbcc

#specify your own color file
$ namethatcolor -c path/to/color/file aabbcc

As a library:

>>> from namethatcolor import NameThatColor
>>> Namer = NameThatColor()
>>> Namer.name('aabbcc')
Match('#B0C4DE', 'lightsteelblue', False, '#AABBCC')
>>> resene_filename = NameThatColor.color_sets['resene']
>>> resene_colors = NameThatColor.get_color_file(resene_filename)
>>> Namer = NameThatColor(color_file=resene_colors)
>>> Namer.name('aabbcc')
Match('#ADBED1', 'Casper', False, '#AABBCC')
"""
import json
from collections import namedtuple

ColorInfo = namedtuple('ColorInfo',
                       ' '.join(['hex_value', 'name', 'red', 'green', 'blue',
                                 'hue', 'saturation', 'lightness']))
RGB = namedtuple('RGB', ' '.join(['red', 'green', 'blue']))
HSL = namedtuple('HSL', ' '.join(['hue', 'saturation', 'lightness']))

class Match(object):
    default_format = 'json'
    default_output = ['hex_value', 'name']

    formats = {
        'json': lambda r: json.dumps(
            dict([(k, r.__dict__[k]) for k in r.output])),
        'raw' : lambda r: repr(r)
    }

    outputs = ['hex_value', 'name', 'exact', 'original']

    def __init__(self, hex_value, name, exact, original, format=None,
                 output=None):
        if format is None:
            format = self.default_format
        if output is None:
            output = self.default_output

        self.output = output
        self.format = format
        self.hex_value = hex_value
        self.name = name
        self.exact = exact
        self.original = original

    def __repr__(self):
        return "Match('%s', '%s', %s, '%s')" % (
            self.hex_value, self.name, self.exact, self.original)

    def __str__(self):
        return self.formats[self.format](self)

class NameThatColor(object):
    """Utility for finding the closest "human readable" name for a hex color
    """
    default_color_set = 'css3'

    color_sets = {
        'resene': 'resene.csv',
        'html4': 'html4.csv',
        'css3': 'css3.csv'
    }

    def __init__(self, color_file=None, format=None, output=None):
        if color_file is None:
            color_file = self.get_color_file(
                self.color_sets[self.default_color_set])

        self.color_info = []

        if format is not None:
            Match.default_format = format
        if output is not None:
            Match.default_output = output

        with open(color_file, 'r') as color_handle:
            for line in filter(lambda l: l.startswith('#'),
                               color_handle.readlines()):
                #there may be commas in names. this is a little sloppy.
                parts = line.split(',')
                hex_val = parts[0]
                name = ','.join(parts[1:])

                red, green, blue = self.rgb(hex_val.strip())
                hue, saturation, lightness = self.hsl(hex_val.strip())
                self.color_info.append(ColorInfo(hex_val.strip(), name.strip(),
                                                 red, green, blue,
                                                 hue, saturation, lightness))
    @classmethod
    def get_color_file(cls, color_file):
        from pkg_resources import Requirement, resource_filename
        return resource_filename(
            Requirement.parse('namethatcolor'),
            'namethatcolor/data/%s' % color_file)
    

    def name(self, color):
        """Return the closest human readable name given a color
        """
        color = color.upper()

        if not 3 < len(color) < 8:
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
        the_color = None
        df = -1

        for info in self.color_info:
            if color == info.hex_value:
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

        if not the_color.name:
            return Match("#000000", "Invalid Color", False, color)
        else:
            return Match(the_color.hex_value, the_color.name, False, color)

    def rgb(self, color):
        """Given a hex string representing a color, return an object with
        values representing red, green, and blue.
        """
        return RGB(int(color[1:3], 16),
                   int(color[3:5], 16),
                   int(color[5:7], 16))

    def hsl(self, color):
        """Given a hex string representing a color, return an object with
        attributes representing hue, lightness, and saturation.
        """

        red, green, blue = self.rgb(color)

        red /= 255.0
        green /= 255.0
        blue /= 255.0

        min_color = min(red, min(green, blue))
        max_color = max(red, max(green, blue))
        delta = max_color - min_color
        lightness = (min_color + max_color) / 2

        saturation = 0
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

def main():
    """Entry point for NameThatColor.py.
    Parse options, and find that color.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find the closest known color name for a hex value")

    color_set_sources = parser.add_mutually_exclusive_group()

    color_set_sources.add_argument('-s', '--color-set', dest="color_set",
                                   choices=NameThatColor.color_sets.keys(),
                                   default=NameThatColor.default_color_set,
                                   help="the set of color names to match to.")

    color_set_sources.add_argument('-c', '--colors', dest='colors_file',
                                   help="a csv file colors and their hex value")

    parser.add_argument('-o', '--output',
                        dest="output",
                        nargs='*',
                        choices=Match.outputs,
                        default=Match.default_output,
                        help="what information about the color match to output")

    parser.add_argument('--format',
                        dest="format",
                        choices=Match.formats.keys(),
                        default=Match.default_format,
                        help="what format to return data in")

    parser.add_argument('target',
                        help="hex value of the color to search for")

    args = parser.parse_args()

    colors_file = args.colors_file

    if not colors_file:
        colors_file = NameThatColor.get_color_file(
            NameThatColor.color_sets[args.color_set])
        
    Namer = NameThatColor(colors_file, args.format, args.output)
    print(Namer.name(args.target))


if __name__ == '__main__':
    main()
