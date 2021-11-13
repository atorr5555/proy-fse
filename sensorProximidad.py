from gpiozero import DistanceSensor,LED
import telebot
#leer el txt para el modo seguro

sensor = DistanceSensor(echo=24, trigger=23, max_distance=1, threshold_distance=0.2)
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño

while True:
    fic = open('base.txt', "r")
    base = []

    for line in fic:
        base.append(line)

    fic.close()
    #leer el txt para saber si es de día o de noche
    #dependiendo de si el modo seguro esta activado puede o no abrir la puerta de manera automatica y prender la luz
    if((sensor.distance * 100) < 15):
        if(base[0]=="modoSeguro=False"):
            #abrir la puerta
        else:
            bot.send_message('-683852329','Se detecto movimiento, Alarma ENCENDIDA')
            #prender la alarma 
            f = open('base.txt')
            Apagado=f.read()
            f.close()
            while Apagado:
                pass
            if(base[1]):
                #prende la luz 
                leds[0].value = 1
                leds[1].value = 1  
    else:
        pass
        

