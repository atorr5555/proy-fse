from gpiozero import PWMLED, Button
from time import sleep

leds = [PWMLED(17), PWMLED(27)]
buttonCuarto = Button(3)
buttonBaño = Button(2)

#Switch
while True:
    #Revisar "base" para verificar alteraciones por telegram
    f = open("leds.txt")
    arregloBase=f.read()
    f.close()
    arregloBase = anterior if len(arregloBase) == 0 else arregloBase.split(sep=',')
    arregloBase = [ int(x) for x in arregloBase ]

    leds[0].value = arregloBase[0]
    leds[1].value = arregloBase[1]

    if(buttonBaño.is_pressed):
        if(leds[0].value==0):
            leds[0].value=1
            arregloBase[0] = 1
        else:
            leds[0].value=0
            arregloBase[0] = 0
        sleep(1)

    if(buttonCuarto.is_pressed):
        if(leds[1].value==0):
            leds[1].value=1
            arregloBase[1] = 1
        else:
            leds[1].value=0
            arregloBase[1] = 0
        sleep(1)

    f = open("leds.txt", 'w')
    f.write(str(arregloBase[0]) + ',' + str(arregloBase[1]))
    f.close()
    anterior = arregloBase