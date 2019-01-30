#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message, textsize
# from myinitfont import text, show_message, textsize
from luma.core.legacy.font import  proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from .myfont import MINI_FONT, DRAWING_FONT
import numpy as np
from .arborescence_menu import MENU_TREE
from PIL import Image, ImageDraw, ImageFont
# PIL.ImageFont.truetype(font=None, size=10, index=0, encoding='', layout_engine=None)
from .Methodes import AnimateText, MenuNavigation, AnimateFigures


""" device methodes :
    Screen.device.  :
        display
        contrast
        """


class LEDMatrix() :
    def __init__(self) :

        parser = argparse.ArgumentParser(description='matrix_demo arguments',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)


        parser.add_argument('--width', type=int, default=8, help='Width')
        parser.add_argument('--height', type=int, default=8, help='height')
        parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
        parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotation factor')

        args = parser.parse_args()

        # create matrix device
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded= 4, rotate=args.rotate, block_orientation=args.block_orientation)
        self.device.contrast(1)

        self.Animatext = AnimateText(self.device)
        self.Menu = MenuNavigation(self.device)
        self.Animafig = AnimateFigures(self.device) 
   
        print("ici")

    #############################################################################################################"#

if __name__ == "__main__":

    Screen = LEDMatrix()
    #Screen.Animatext.Slice()
    #time.sleep(1)
    Screen.Animatext.Static("slt")
    #for contrast in range(255) :
    #    Screen.device.contrast(contrast)
    #    time.sleep(0.1)
    Screen.Animatext.Rolling("salut tout le monde les gens")
    Screen.Animafig.Dessin("abcdefg")
    time.sleep(1)
    #Screen.Animafig.printText("slt")
    Screen.Static.draw("menu")
    while 1 :
        Screen.Menu.Navigate()
