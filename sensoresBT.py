from gpiozero import DistanceSensor, PWMLED,DistanceSensor,Servo
import telebot
from bluedot import BlueDot
import Adafruit_DHT 
import os
from time import sleep

bd = BlueDot()
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
servo=Servo(4)
sensorTemp=Adafruit_DHT.DHT11
API_TOKEN=""
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=False
banderaViolacion=False
#sensor = DistanceSensor(echo=24, trigger=23)

#TXT o base de datos [modo_seguro,banderaViolacion]
f = open("base.txt")
arregloBase=f.read()
f.close()

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
        while((sensor.distance * 100)<10):
            servo.max()
        servo.min()
        print('CERRADA')

def checarAlarma():
    if(modo_seguro and banderaViolacion):
        os.system("sudo python ~/lightshowpi/py/synchronized_lights.py --file=/home/pi/Downloads/sonido.mp3")

def comando(pos):
    if pos.middle:
        #Llamado al asistente con bandera de solo 1 instruccion
        os.system("python pushtotalk.py --once")
   

while True:
    #Revisar "base" para verificar alteraciones por telegram
    f = open("base.txt")
    arregloBase=f.read()
    f.close()
    print(arregloBase)
    arregloBase = arregloBase.split(sep=',')

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
    #if((sensor.distance * 100)<10):
        #turnon()

    #Cuando la seguridad haya sido violada seguir activando la alarma
    checarAlarma()