from machine import Pin, PWM
from time import sleep

B_PIN = 33
buzzer_pin = Pin(B_PIN, Pin.OUT)
pwm_buzz = PWM(buzzer_pin)

# shut up buzz
pwm_buzz.duty(0)

def buzzer(buzzerPinObject, frequency, sound_duration, silence_duration):
    buzzerPinObject.duty(512)
    buzzerPinObject.freq(frequency)
    sleep(sound_duration)
    buzzerPinObject.duty(0)
    sleep(silence_duration)



def buzzer_play():
    buzzer(pwm_buzz, 150, 1.5, 0.3)
    buzzer(pwm_buzz, 150, 1.5, 0.3)
    buzzer(pwm_buzz, 150, 1.5, 0.3)
   
