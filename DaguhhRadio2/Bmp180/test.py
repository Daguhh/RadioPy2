from BMP180 import BMP180

# I2C bus=1, Address=0x77
bmp = BMP180(1, 0x77)

p = bmp.pressure()  # read pressure
print(p)            # namedtuple
print(p.hPa)        # hPa value

t = bmp.temperature()  # read temperature
print(t)               # namedtuple
print(t.C)             # Celcius degree

p, t = bmp.all()  # read both at once
print(p)          # Pressure namedtuple
print(t)          # Temperature namedtuple

# Look up mean sea level pressure from local observatory.
# 1009.1 hPa is only for example.
a = p.altitude(msl=1009.1)

print(a)     # Altitude
print(a.m)   # in metre
print(a.ft)  # in feet
