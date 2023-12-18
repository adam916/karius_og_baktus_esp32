from machine import Pin, SoftI2C
import time

# MLX90614 I2C address
MLX90614_I2C_ADDR = 0x5A

# MLX90614 register addresses
MLX90614_TA = 0x06  # Ambient temperature
MLX90614_TOBJ1 = 0x07  # Object temperature

# Define I2C pins
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

def read_temperature(reg):
    # Read 2 bytes from the specified register
    data = i2c.readfrom_mem(MLX90614_I2C_ADDR, reg, 2)
    # Convert the bytes to temperature value (Celsius)
    temperature = (data[1] << 8 | data[0]) * 0.02 - 273.15
    return temperature


# test
'''
while True:
    # Read ambient temperature
    ambient_temp = read_temperature(MLX90614_TA)
    #rint("Ambient temperature: {:.2f} °C".format(ambient_temp))

    # Read object temperature
    object_temp = read_temperature(MLX90614_TOBJ1)
    #print("Object temperature: {:.2f} °C".format(object_temp))
    print(object_temp, ambient_temp)


    time.sleep(1)  # Adjust the sleep time as needed
'''