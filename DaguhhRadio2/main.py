#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 12:40:03 2017

@author: david
"""

import time

from Rotary_Encoder import RotaryEncoder, ButtonEncoder
from LED_Matrix import LEDMatrix
from TEARadio import Tea5767
from RTC_DS1307 import DS1307

Screen = LEDMatrix()
Encodeur = RotaryEncoder()
BE = ButtonEncoder()
Radio = Tea5767()
RTC = DS1307()

Screen.Animatext.Slice("hello")
time.sleep(0.5)

temp=str(RTC.get_full_hour())
print(temp)
Screen.Animatext.Rolling(temp)


if 0 :
    while True :
        
        Encodeur.count()
        print("count= " + str(Encodeur.counter))
        print("direction= " + str(Encodeur.direction))
        print("state= " + str(BE.State()))
        
        if Encodeur.direction == 1 :
            Screen.Menu.Navigate("z")
        elif Encodeur.direction == -1 :
            Screen.Menu.Navigate("s")
        
if 1 :
    frequence = 92.5
    while True :
        Encodeur.count()
        
        if Encodeur.direction == 1 :
            frequence += 0.1
        elif Encodeur.direction == -1 :
            frequence -= 0.1
        Radio.setFreq(frequence*10**6)
        Screen.Animatext.Static('{:5.1f}'.format(frequence))






        
        


        
