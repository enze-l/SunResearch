from machine import Pin, I2C
from bh1750 import BH1750


s = BH1750(I2C(scl=Pin(22), sda=Pin(21)))

while True:
    s.luminance(BH1750.ONCE_HIRES_2)