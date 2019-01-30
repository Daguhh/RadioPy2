#!/usr/bin/python3
from smbus2 import SMBus
import datetime
import random


class DS1307():
    def __init__(self):
        # I2C Address of DS1307 RTC
        self.i2c = SMBus(1)
        self.ds1307addr = 0x68
    
    # Functions for getting and setting according to the DS1307 Datasheet
    def ds1307_get_seconds(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x00)
        	lower4bits = retbyte & 0b00001111
        	upper4bits = ((retbyte & 0b01110000) >> 4)
        	returnstr = str(upper4bits) + str(lower4bits)
        	return int(returnstr)
    	
    def ds1307_get_minutes(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x01)
        	lower4bits = retbyte & 0b00001111
        	upper4bits = ((retbyte & 0b01110000) >> 4)
        	returnstr = str(upper4bits) + str(lower4bits)
        	return int(returnstr)	
    
    # Returns in 24 hours mode
    def ds1307_get_hours(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x02)
        	lower4bits = retbyte & 0b00001111
        	# Check if 24 Hour Clock
        	mode12 = ((retbyte & 0b01000000) >> 6)
        	if mode12 == 0:
        		# 24-hour-mode
        		upper4bits = ((retbyte & 0b00110000) >> 4)
        		returnstr = str(upper4bits) + str(lower4bits)
        		return int(returnstr)	
        	else:
        		# 12-hour-mode
        		upper4bits = ((retbyte & 0b00010000) >> 4)
        		returnstr = str(upper4bits) + str(lower4bits)
        		pm_am = ((retbyte & 0b00100000) >> 5)
        		if pm_am == 1:
        			# pm - we return in 24-hour-mode
        			return int(returnstr) + 12
        		else:
        			# am
        			return int(returnstr)
    
    def ds1307_get_day(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x03)
        	lower3bits = retbyte & 0b00000111
        	returnstr = str(lower3bits)
        	return int(returnstr)		
    
    def ds1307_get_date(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x04)
        	lower4bits = retbyte & 0b00001111
        	upper4bits = ((retbyte & 0b00110000) >> 4)
        	returnstr = str(upper4bits) + str(lower4bits)
        	return int(returnstr)		
    
    def ds1307_get_month(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x05)
        	lower4bits = retbyte & 0b00001111
        	upper4bits = ((retbyte & 0b00010000) >> 4)
        	returnstr = str(upper4bits) + str(lower4bits)
        	return int(returnstr)		
    
    def ds1307_get_year(self):
        	retbyte = self.i2c.read_byte_data(self.ds1307addr, 0x06)
        	lower4bits = retbyte & 0b00001111
        	upper4bits = ((retbyte & 0b11110000) >> 4)
        	returnstr = str(upper4bits) + str(lower4bits)
        	returnval = int(returnstr)	
        	if returnval > 60:
        		# year 60 - 99 must be 1900
        		return returnval + 1900
        	else:
        		# year 00 - 60 must be 2000
        		return returnval + 2000
    
    # Returns: Clock stopped, 12-hour-mode, outputmode, squarewaveenabled, frequency as a five value tuple
    def ds1307_get_control(self):
        	retbyte1 = self.i2c.read_byte_data(self.ds1307addr, 0x00)
        	retbyte2 = self.i2c.read_byte_data(self.ds1307addr, 0x02)
        	retbyte3 = self.i2c.read_byte_data(self.ds1307addr, 0x07)
        	clockstopped = ((retbyte1 & 0b10000000) >> 7)
        	mode12 = ((retbyte2 & 0b01000000) >> 6)
        	out = ((retbyte3 & 0b10000000) >> 7)
        	sqwe = ((retbyte3 & 0b00010000) >> 4)
        	rs0 = ((retbyte3 & 0b00000001) >> 0)
        	rs1 = ((retbyte3 & 0b00000010) >> 1)
        	if rs1 == 0 and rs0 == 0:
        		freq = 1
        	if rs1 == 0 and rs0 == 1:
        		freq = 4096000
        	if rs1 == 1 and rs0 == 0:
        		freq = 8192000
        	if rs1 == 1 and rs0 == 1:
        		freq = 32768000
        	return clockstopped, mode12, out, sqwe, freq
        	
        # Valid addr for RAM: 0 - 55
    def ds1307_get_ram(self,addr):
        #RAM starts at Address 0x08
        addr = addr + 0x08	
        return self.i2c.read_byte_data(self.ds1307addr, addr)	
    	
   
    def get_full_hour(self):
        seconds = self.ds1307_get_seconds()
        minutes = self.ds1307_get_minutes()
        hours = self.ds1307_get_hours()
        full_hour = ("{}:{}:{}").format(hours,minutes,seconds)
        return full_hour
  