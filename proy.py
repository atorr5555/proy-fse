from gpiozero import DistanceSensor, LED, PWMLED
from signal import pause
import telebot
from time import sleep
from bluedot import BlueDot

#Definimos las varibale a utilizar en las diferentes funciones del proyecto WORKY
bd = BlueDot()
sensor = DistanceSensor(echo=24, trigger=23, max_distance=1, threshold_distance=0.2)
leds = [PWMLED(17), PWMLED(27)] #Los de cuarto y baño
API_TOKEN="2062315514:AAGhE-cja5Cvot5PDiBoi5I-y4OZuIZgQPU"
bot=telebot.TeleBot(API_TOKEN)
modo_seguro=True
intruso=True
password="default"

#FUNCIONES para las caracteristicas de WORKY
def inRange():
    led.on()
    #bot.send_message('1157726974','Se detecto movimiento, Alarma ENCENDIDA')
    #bot.send_message('@atorr55','Se detecto movimiento, Alarma ENCENDIDA')
    bot.send_message('-683852329','Se detecto movimiento, Alarma ENCENDIDA')
    return True
    
def outOfRange():
    led.off()
    return True

def encender(intruso):
    while intruso:
        print('Distance: ', sensor.distance * 100)
        if((sensor.distance * 100) < 15):
            intruso=False
            inRange()
        else:
            outOfRange()

def comando(pos):
    if pos.bottom:
        led = 0
        if(pos.x>0):
            leds[0].value = 0
            led=1 #Enciende luz de cuarto
        if(pos.x<0):
            leds[1].value = 0
            led=0 #Enciende luz de baño
        brightness = (pos.y + 1) / 2
        leds[led].value = brightness
    elif pos.top:
        pass#Comando para activar el asistente


#Intrucciones ingresadas por medio de TELEGRAM escrito
@bot.message_handler(commands=['Cambiar_contraseña'])
def send_welcome(message):
    bot.reply_to(message, """\
Se modifico la contraseña de modo seguro
""")
    password=message.text.split()[1:][0]
    print(password)

@bot.message_handler(commands=['Desactivar_seguridad'])
def send_welcome(message):
    bot.reply_to(message, """\
Modo Seguro Apagado
""")
    modo_seguro=False
    
@bot.message_handler(commands=['Activar_Seguridad'])
def send_welcome(message):
    mensaje = ''
    if(message.text.split()[1:][0]==password):
        modo_seguro=True
        mensaje="Se Activo el modo seguro"
    else:
        mensaje="Contraseña incorrecta"
    bot.reply_to(message, """\
"""+mensaje)
    

@bot.message_handler(commands=['encender'])
def send_welcome(message):
    bot.reply_to(message, """\
Alarma Encendida
""")
    intruso=True
    encender(intruso)

#Ejecucion por medio de BLUEDOT 
bd.when_pressed = Comando

#Mantener siempre activo al bot programa en eterna ejecución
bot.infinity_polling()


    