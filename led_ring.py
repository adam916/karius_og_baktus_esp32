import neopixel
from machine import Pin
import time

p = 15
n = 12
np = neopixel.NeoPixel(Pin(p), n)
green = (0,15,0) 
red = (15,0,0)
blue = (0,0,15)
yellow = (15,15,2)
off = (0,0,0)

# wifi connection indication
def led_connect():
    for i in range(2):
        for i in range(n):
            np[i] = blue
            np.write()
            np[i] = off
            time.sleep(0.05)
    led_red()


def led_red():
    for i in range(n):
        np[i] = red
        np.write()

def led_green():
    for i in range(n):
        np[i] = green
        np.write()
        
def led_blue():
    for i in range(n):
        np[i] = blue
        np.write()

def led_off():
    for i in range(n):
        np[i] = off
        np.write()

# brush time indicator
def led_brush(count):
    if count <= 4:     
            np[count] = red
            np.write()
            
    if count > 4 and count <= 8:
            np[count] = yellow
            np.write()
            
    if count > 8 and count < 12:
            np[count] = green
            np.write()


def led_blink():
    for i in range(2):
        led_blue()
        time.sleep(0.5)
        led_off()
        time.sleep(0.5)