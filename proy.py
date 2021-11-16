from gpiozero import DistanceSensor, PWMLED,MotionSensor,Servo,Button
from signal import pause
import telebot
from time import sleep
from bluedot import BlueDot
import subprocess
from multiprocessing import Process,Queue,Pipe
import os
import Adafruit_DHT 

#Definimos las varibale a utilizar en las diferentes funciones del proyecto WORKY
bd = BlueDot()
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
pir = MotionSensor(21)
buttonCuarto = Button(2)
buttonBaño = Button(3)
servo=Servo(4)
sensorTemp=Adafruit_DHT.DHT11
API_TOKEN="2132027653:AAHT4NyCbrFJIH5kLcbd4oB5GioUQZik0Z8"
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=False
banderaViolacion=False

#FUNCIONES para las caracteristicas de WORKY
def inRange():
    led[0].on()
    #bot.send_message('1157726974','Se detecto movimiento, Alarma ENCENDIDA')
    #bot.send_message('@atorr55','Se detecto movimiento, Alarma ENCENDIDA')
    bot.send_message('-683852329','Se detecto movimiento, Alarma ENCENDIDA')
    return True
    
def outOfRange():
    led[0].off()
    return True

def turnon():
    print('TURN OONN')
    print(modo_seguro)
    if(modo_seguro):
        bot.send_message('-683852329','Se detecto movimiento, Alarma ENCENDIDA')
        os.system("sudo python ~/lightshowpi/py/synchronized_lights.py --file=/home/pi/Downloads/sonido.mp3")
        banderaViolacion=True
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

#Intrucciones ingresadas por medio de TELEGRAM escrito
@bot.message_handler(commands=['Desactivar_seguridad'])
def send_welcome(message):
    modo_seguro=False
    banderaViolacion=False
    bot.reply_to(message, """\
Modo Seguro Apagado
""")
    
@bot.message_handler(commands=['Activar_Seguridad'])
def send_welcome(message):
    modo_seguro=True
    mensaje="Se Activo el modo seguro"
    bot.reply_to(message, """\
"""+mensaje)

@bot.message_handler(commands=['ApagarCuarto'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del cuarto
""")
    leds[1].value=0

@bot.message_handler(commands=['ApagarBaño'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del baño
""")
    leds[0].value=0

@bot.message_handler(commands=['ApagarLuces'])
def send_welcome(message):
    bot.reply_to(message, """\
/EncenderBaño
""")
    #bot.reply_to(message, """\
#Se ajusto la luz del baño
#""")
    leds[0].value=0
    leds[1].value=0

@bot.message_handler(commands=['DatosAmbientales'])
def send_welcome(message):
    humedad,temp = Adafruit_DHT.read_retry(sensorTemp,26)
    bot.reply_to(message, 
"La temperatura de la habitacion es: "+ str(temp) +" grados "+" y su humedad: "+ str(humedad)
)
    
@bot.message_handler(commands=['EncenderCuarto'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del cuarto
""")
    if(len(message.text)==15):
        leds[1].value=1
    else:
        valor=message.text.split()[1:][0]
        leds[1].value=int(valor)/100

@bot.message_handler(commands=['EncenderBaño'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del baño
""")
    print(message.text)
    print(len(message.text))
    if(len(message.text)==13):
        leds[0].value=1
    else:
        valor=message.text.split()[1:][0]
        leds[0].value=int(valor)/100


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

#Mantener siempre activo al bot programa en eterna ejecución
bot.infinity_polling()


    