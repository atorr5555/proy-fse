from gpiozero import DistanceSensor, PWMLED,DistanceSensor,Servo
import telebot
from bluedot import BlueDot
import Adafruit_DHT 
import os
from time import sleep
import tokens
import RPi.GPIO as GPIO
import time

bd = BlueDot()
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
servo=Servo(4)
sensorTemp=Adafruit_DHT.DHT11
API_TOKEN=tokens.token
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=False
banderaViolacion=False
sensor = DistanceSensor(echo=20, trigger=16)
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#TXT o base de datos [modo_seguro,banderaViolacion]
f = open("base.txt")
arregloBase=f.read()
f.close()

def callback(channel):
    bot.send_message('-683852329','FUEGO DETECTADO. ALERTA')

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

#Funciones
def turnon():
    if(modo_seguro):
        bot.send_message('-683852329','Se detecto movimiento, Alarma ENCENDIDA')
        os.system("sudo python ~/lightshowpi/py/synchronized_lights.py --file=/home/pi/Downloads/sonido.mp3")
        banderaViolacion=True
        with open('base.txt', 'w') as f:
            f.write('True,True')
    else:
        servo.max()
        print('ABIERTA')
        sleep(2)
        while((sensor.distance * 100)<10):
            servo.max()
            sleep(2)
        servo.min()
        print('CERRADA')

def checarAlarma():
    if(modo_seguro and banderaViolacion):
        os.system("sudo python ~/lightshowpi/py/synchronized_lights.py --file=/home/pi/Downloads/sonido.mp3")

def comando(pos):
    if pos.middle:
        #Llamado al asistente con bandera de solo 1 instruccion
        f = open("leds.txt")
        arregloBase=f.read()
        f.close()
        arregloBase = arregloBase.split(sep=',')
        arregloBase = [ int(x) for x in arregloBase ]
        arregloBase[0] = leds[0].value
        arregloBase[1] = leds[1].value
        f = open("leds.txt", 'w')
        f.write(str(arregloBase[0]) + ',' + str(arregloBase[1]))
        f.close()
        os.system("python pushtotalk.py --once")
        f = open("leds.txt")
        arregloBase=f.read()
        f.close()
        arregloBase = arregloBase.split(sep=',')
        arregloBase = [ int(x) for x in arregloBase ]
        leds[0].value = arregloBase[0]
        leds[1].value = arregloBase[1]
   

while True:
    #Revisar "base" para verificar alteraciones por telegram
    f = open("base.txt")
    arregloBase=f.read()
    f.close()
    arregloBase = anterior if len(arregloBase) == 0 else arregloBase.split(sep=',')

    if(arregloBase[0]=='True'):
        modo_seguro=True
    else:
        modo_seguro=False

    if(arregloBase[1]=='True'):
        banderaViolacion=True
    else:
        banderaViolacion=False

    #Ejecucion por medio de BLUEDOT 
    bd.when_pressed = comando

    #Sensor de proximidad
    if((sensor.distance * 100)<10):
        print(sensor.distance*100)
        turnon()

    #Cuando la seguridad haya sido violada seguir activando la alarma
    checarAlarma()
    anterior = arregloBase