from gpiozero import DistanceSensor, PWMLED,MotionSensor,Servo,Button
from gpiozero import DistanceSensor, PWMLED,MotionSensor,Servo,Button
import telebot
from bluedot import BlueDot
import Adafruit_DHT 
import os

bd = BlueDot()
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
pir = MotionSensor(21)
buttonCuarto = Button(2)
buttonBaño = Button(3)
servo=Servo(4)
sensorTemp=Adafruit_DHT.DHT11
API_TOKEN=""
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=False
banderaViolacion=False

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
        while(not(pir.motion_detected)):
            servo.max()
        servo.min()
        print('CERRADA')

def checarAlarma():
    if(modo_seguro and banderaViolacion):
        os.system("sudo python ~/lightshowpi/py/synchronized_lights.py --file=/home/pi/Downloads/sonido.mp3")

def comando(pos):
    if pos.bottom:
        led = 0
        if(pos.x>0):
            led=1 #Enciende luz de cuarto
        if(pos.x<0):
            led=0 #Enciende luz de baño
        brightness = (pos.y + 1) / 2
        leds[led].value = brightness
    elif pos.top:
        #Llamado al asistente con bandera de solo 1 instruccion
        subprocess.call("python pushToTalk.py --once", shell=True)

while True:
    #Revisar "base" para verificar alteraciones por telegram
    f = open("base.txt")
    arregloBase=f.read()
    f.close()
    arregloBase.split(sep=',')

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
    pir.when_motion=turnon

    #Cuando la seguridad haya sido violada seguir activando la alarma
    checarAlarma()

    #Switch
    if(buttonBaño.is_pressed):
        if(leds[0].value==0):
            leds[0].value=1
        else:
            leds[0].value=0

    if(buttonCuarto.is_pressed):
        if(leds[1].value==0):
            leds[1].value=1
        else:
            leds[1].value=0