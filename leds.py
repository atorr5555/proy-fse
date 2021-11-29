from gpiozero import PWMLED, Button
from time import sleep

leds = [PWMLED(17), PWMLED(27)]
buttonCuarto = Button(3)
buttonBaño = Button(2)

#Switch
while True:
    if(buttonBaño.is_pressed):
        if(leds[1].value==0):
            leds[1].value=1.0
        else:
            leds[1].value=0.0
        sleep(1)

    if(buttonCuarto.is_pressed):
        if(leds[0].value==0):
            leds[0].value=1.0
        else:
            leds[0].value=0.0
        sleep(1)