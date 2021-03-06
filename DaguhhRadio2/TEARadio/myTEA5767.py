#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import RPi.GPIO as GPIO

from smbus2 import SMBus
from smbus2 import SMBusWrapper
import time
import numpy as np


'''
# SMBbus main functions
from smbus2 import SMBus

# Open i2c bus 1 and read one byte from address 80, offset 0
bus = SMBus(1)

b = bus.read_byte_data(80, 0)
print(b)
bus.close()

# =============   read a byte   ====================
from smbus2 import SMBusWrapper

with SMBusWrapper(1) as bus:
    b = bus.read_byte_data(80, 0)
    print(b)

# =============   write a byte ======================

from smbus2 import SMBusWrapper

with SMBusWrapper(1) as bus:
    # Write a byte to address 80, offset 0
    data = 45
    bus.write_byte_data(80, 0, data)

# ============ bloc of data ==========================
from smbus2 import SMBusWrapper

with SMBusWrapper(1) as bus:
    # Read a block of 16 bytes from address 80, offset 0
    block = bus.read_i2c_block_data(80, 0, 16)
    # Returned value is a list of 16 bytes
    print(block)


from smbus2 import SMBusWrapper

with SMBusWrapper(1) as bus:
    # Write a block of 8 bytes to address 80 from offset 0
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bus.write_i2c_block_data(80, 0, data)

'''

class Tea5767 :
    def __init__(self):
        self.bus = SMBus(1)
        self.addr = 0x60

        self.Fif = 225000
        self.Fref = 32768
        # ==================   Parameter ==========================================
        # while writing bytes
        # 1st byte
        self.mute = 0 # 1 for mute                                              # 7
        self.search_mode = 0  # 1 for search mode                               # 6

        # 1st and 2nd byte
        self.PLL = 12234                                                       # 5-0 and 7-0

        # 3rd byte
        self.search_direction = 1                                               # 7
        self.search_stop_level = np.array([0,1], dtype=np.int8)                 # 6-5
        self.side_injection = 1                                                 # 4
        self.mono = 0  # force mono                                             # 3
        self.mute_right = 0                                                     # 2
        self.mute_left = 0                                                      # 1
        self.port1 = 0  # check ready signal                                    # 0

        # 4th byte
        self.port2 = 0                                                          # 7
        self.stanby_mode = 0                                                    # 6
        self.band_limit = 0 # 0 for europe                                      # 5
        self.clock_freq = 1 # 0 for 13MHz /  1 for 32.768kHz   let PLLREF to 0  # 4
        self.soft_mute = 0                                                     # 3
        self.high_cut_control = 0                                               # 2
        self.stereo_noise_cancelling = 1                                        # 1
        self.search_indicator = 1 # make port1 an output for readyflag          # 0

        # 5th byte
        self.pllref = 0 # 1 to enable external clock reference at 6.5MHz        # 7
        self.dtc = 0 # change de-emphasis time constant                         # 6

        # while reading bytes
        # 1st byte
        self.ready_flag = 0 # station have been found                           # 7
        self.band_limit_flag = 0 # band limit reached                           # 6
        # next = pll

        # 3rd byte
        # stereo  => use self.mono                                              # 7
        self.IF_counter_result = 0 # pas compris    intermediate freq           # 6-0

        # 4th byte
        self.output_level = np.array([0,0,0], dtype=np.int8)                    # 7-4
        self.chip_ID = np.array([0,0,0], dtype=np.int8)                         # 3-1

        # 5th byte = always 0

        # ==================   Initialise  ==========================================
        self.makeByte()
        self.writeBytes()


    def isReady(self) :
        '''
        self.port1 = value

        The software programmable output (SWPORT1) can be programmed to operate as a
        tuning indicator output. As long as the IC has not completed a tuning action,
        pin SWPORT1 remains LOW. The pin becomes HIGH, when a preset or search tuning is
        completed or when a band limit is reached.

        '''


    def makeByte(self) :

        self.block = np.zeros(5, dtype = np.int32)

        self.block[0] =  self.mute*2**7 
        self.block[0] += self.search_mode*2**6 
        self.block[0] += self.PLL // 2**8 

        self.block[1] = self.PLL % 2**8

        self.block[2] =  2**7 * self.search_direction 
        self.block[2] += 2**6 * self.search_stop_level[0] 
        self.block[2] += 2**5 * self.search_stop_level[1]
        self.block[2] += 2**4 * self.side_injection 
        self.block[2] += 2**3 * self.mono 
        self.block[2] += 2**2 * self.mute_right 
        self.block[2] += 2**1 * self.mute_left 
        self.block[2] += 2**0 * self.port1

        self.block[3] =  2**7 * self.port2 
        self.block[3] += 2**6 * self.stanby_mode  
        self.block[3] += 2**5 * self.band_limit 
        self.block[3] += 2**4 * self.clock_freq  
        self.block[3] += 2**3 * self.soft_mute  
        self.block[3] += 2**2 * self.high_cut_control  
        self.block[3] += 2**1 * self.stereo_noise_cancelling  
        self.block[3] += 2**0 * self.search_indicator

        self.block[4] =  2**7 * self.pllref 
        self.block[4] += 2**6 * self.dtc

        print("makeBytes = " + str(self.block))

    def getFreq(self):
        block = self.readBytes()
        PLL_H = block[0] % (2**6) * 2**8
        PLL_L = block[1]
        Npll= PLL_H + PLL_L
        print("get : " + str(Npll))
        F_rf= (Npll * self.Fref / 4) - self.Fif  
        return F_rf


    def setFreq(self,newFreq, mute = 0, search_mode = 0) :
        self.PLL = int( 4 * (newFreq + self.Fif)  / self.Fref )
        print("set : " + str(self.PLL))
        self.makeByte()
        self.writeBytes()


    def readBytes(self):
        with SMBusWrapper(1) as bus:  
            block = self.bus.read_i2c_block_data(self.addr, self.block[0], 5)
        return block


    def writeBytes(self):
        data = self.block
        with SMBusWrapper(1) as bus:
            self.bus.write_i2c_block_data(self.addr, data[0], data[1::])


if __name__ == "__main__" :  
    TEA = tea5767()
    time.sleep(1)
    TEA.writeBytes()
    time.sleep(1)
    B = TEA.readBytes()
    TEA.setFreq(102.5*10**6)
    freq = 92.5*10**6
    while 1 :
        a=input()
        if a == "-" :
            freq-=0.01*10**6
        elif a == "m" :
            if TEA.mute == 0 :
                TEA.mute = 1
            else :
                TEA.mute = 0
            TEA.makeByte()
        elif a == "s" :
            TEA.search_mode = 1
        else :
            freq+=0.1*10**6
        TEA.setFreq(freq)
        print('===========================================================')
        freq2 = TEA.getFreq()
        print("freq npt = " + str(freq/10**6))
        print("freq msr = " + str(freq2/10**6))
        print("block = " + str(TEA.block))
        print('===========================================================')
    time.sleep(2)
    TEA.bus.close()






