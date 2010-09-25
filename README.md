NameThatColor
=============

Provides a utility for retrieving the closest known "human readable" name for a
color specified as a hex string. It does this by using an algorithm ported from
[ntc.js](http://chir.ag/projects/ntc). 

There are 3 different sets of color definitions to choose from:  
  - [Resene](http://people.csail.mit.edu/jaffer/Color/resenecolours.txt)   
  - [html4](http://www.w3.org/TR/css3-color/#html4)   
  - [css3](http://www.w3.org/TR/css3-color/#svg-color)     

css3 is a superset of html4.

The user can also supply their own colorfile to use. It should be comma
separated hex,name pairs, and should include the leading #. Commas are allowed
in names.

Currently two output formats are supported -- json, and raw. 

Usage:
====== 

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
