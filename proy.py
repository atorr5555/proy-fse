from gpiozero import DistanceSensor, PWMLED,MotionSensor,Servo,Button
import telebot
from time import sleep
import subprocess
from multiprocessing import Process,Queue,Pipe
import Adafruit_DHT 
import os
import tokens
import subprocess

#Definimos las varibale a utilizar en las diferentes funciones del proyecto WORKY
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
pir = MotionSensor(21)
buttonCuarto = Button(2)
buttonBaño = Button(3)
servo=Servo(4)
sensorTemp=Adafruit_DHT.DHT11
API_TOKEN=tokens.token
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=False
banderaViolacion=False


print('PRUEBA')
#TXT o base de datos [modo_seguro,banderaViolacion]
with open('base.txt', 'w') as f:
    f.write('False,False')
# TXT para estado de los leds
with open('leds.txt', 'w') as f:
    f.write('0, 0')

#Arrancar script de sendores
p1=subprocess.Popen(["python", "sensoresBT.py"])
p2=subprocess.Popen(["python", "leds.py"])

def update_leds(led, state):
    f = open("leds.txt")
    arregloBase=f.read()
    f.close()
    arregloBase = arregloBase.split(sep=',')
    arregloBase = [ int(x) for x in arregloBase ]
    arregloBase[led] = state
    f = open("leds.txt", 'w')
    f.write(str(arregloBase[0]) + ',' + str(arregloBase[1]))
    f.close()

#Intrucciones ingresadas por medio de TELEGRAM escrito
@bot.message_handler(commands=['Desactivar_seguridad'])
def send_welcome(message):
    modo_seguro=False
    banderaViolacion=False
    with open('base.txt', 'w') as f:
        f.write('False,False')
    bot.reply_to(message, """\
Modo Seguro Apagado
""")
    
@bot.message_handler(commands=['Activar_Seguridad'])
def send_welcome(message):
    modo_seguro=True
    with open('base.txt', 'w') as f:
        f.write('True,False')
    mensaje="Se Activo el modo seguro"
    bot.reply_to(message, """\
"""+mensaje)

@bot.message_handler(commands=['ApagarCuarto'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del cuarto
""")
    leds[1].value=0
    update_leds(1, 0)

@bot.message_handler(commands=['ApagarBaño'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del baño
""")
    leds[0].value=0
    update_leds(0, 0)

@bot.message_handler(commands=['ApagarLuces'])
def send_welcome(message):
    bot.reply_to(message, """\
Se apagaron las luces
""")
    leds[0].value=0
    leds[1].value=0
    update_leds(0, 0)
    update_leds(1, 0)

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
        update_leds(1, 1)
    else:
        valor=message.text.split()[1:][0]
        leds[1].value=int(valor)/100
        update_leds(1, int(valor)/100)

@bot.message_handler(commands=['EncenderBaño'])
def send_welcome(message):
    bot.reply_to(message, """\
Se ajusto la luz del baño
""")
    print(message.text)
    print(len(message.text))
    if(len(message.text)==13):
        leds[0].value=1
        update_leds(0, 1)
    else:
        valor=message.text.split()[1:][0]
        leds[0].value=int(valor)/100
        update_leds(0, int(valor)/100)

@bot.message_handler(commands=['ayuda', 'help'])
def help(message):
    bot.reply_to(message, """\
Lista de comandos disponibles

EncenderBaño - Enciende la luz del baño
EncenderCuarto - Enciende la luz del cuarto
DatosAmbientales - Muestra la temperatura y humedad
ApagarLuces - Apaga todas las luces
ApagarBaño - Apaga la luz del baño
ApagarCuarto -  Apaga la luz del cuarto
Activar_Seguridad - Activa el modo seguro
Desactivar_seguridad - Desactiva el modo seguro
""")

#Mantener siempre activo al bot programa en eterna ejecución
bot.infinity_polling()

print('MATANDO SUBPROCESOS')
p1.kill()
p2.kill()


    
