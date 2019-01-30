#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 12:40:03 2017

@author: david
"""

from RPi import GPIO
from time import sleep

class ButtonEncoder :
    def __init__(self):
        self.sw = 17
        GPIO.setup(self.sw, GPIO.IN)
        
    def State(self) :
        self.state = GPIO.input(self.sw)
#        print("state = " + str(self.state))
        sleep(0.01)
        return self.state

class RotaryEncoder :
    def __init__(self) :
        self.clk = 22
        self.dt = 27
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.counter = 0
        self.old_counter = 0
        self.direction = 0
        self.clkLastState = GPIO.input(self.clk)

    def count(self) :
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState != self.clkLastState:
            if dtState != clkState:
                self.counter += 1
            else:
                self.counter -= 1
        self.direction = self.counter - self.old_counter
        self.old_counter = self.counter
        self.clkLastState = clkState
        sleep(0.01)


if __name__ == "__main__": 
    a= RotaryEncoder()
    while True :
        print(a.counter)
    

    
    
    
    
####### old version ###########################################"    
#import RPi.GPIO as GPIO

# Initialisation de la numerotation et des E/S

#class Button :
#    def __init__(self, pin):
#        self.pin = pin
#        GPIO.setup(self.pin, GPIO.IN)
#        
#    def State(self) :
#        self.state = GPIO.input(self.pin)
#        return self.state
#        
#    
#class RotaryEncoder :
#    def __init__(self) :
#        GPIO.setmode(GPIO.BCM)
#        
#        self.encoderPosCount = 0
#        self.pinALast = 0
#        self.direction = "None"
#        
#        self.btnSW = Button(23)
#        self.btnCLK = Button(24)
#        self.btnDT = Button(25)
#        
#        self.prev_state = self.btnCLK.State()
#        
#    def State(self) :
#        if self.btnCLK.State() != self.prev_state :
#            # le bouton à tourné
#            if self.btnDT.State() == self.prev_state :
#                self.direction = "clk" # sens horaire
#                self.encoderPosCount += 1
#                print("+1")
#            else :
#                self.direction = "aclk" # sens anti-horaire
#                self.encoderPosCount -= 1
#                print("-1")
#        self.prev_state = self.btnCLK.State()
#        
#        return self.encoderPosCount, self.direction
#
#    def Reset(self) :
#        self.encoderPosCount = 0
#        self.direction = "None"        
#
#test = 1
#ttt = 0
#b=RotaryEncoder()
#while test == 1 :
#    print(b.encoderPosCount)




