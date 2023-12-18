from machine import Pin,ADC
from time import sleep

sensor = ADC(Pin(32))
sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)

number_of_readings = 50

def ldr_reading():
    reading = []
    for i in range(number_of_readings):
        reading.append(sensor.read())
    average_of_readings = sum(reading)/number_of_readings
    average_of_readings = round(average_of_readings)
    #print(average_of_readings)
    return average_of_readings   


'''
while True:
    print(ldr_reading())
    sleep(1)
'''