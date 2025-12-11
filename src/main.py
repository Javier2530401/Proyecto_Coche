from machine import Pin, PWM
import time
import sys

IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
ENA = PWM(Pin(25), freq=1000)

IN3 = Pin(12, Pin.OUT)
IN4 = Pin(13, Pin.OUT)
ENB = PWM(Pin(14), freq=1000)

VELOCIDAD = 60000  

def adelante():
    IN1.value(1); IN2.value(0)
    IN3.value(1); IN4.value(0)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD)

def atras():
    IN1.value(0); IN2.value(1)
    IN3.value(0); IN4.value(1)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD)

def parar():
    IN1.off(); IN2.off()
    IN3.off(); IN4.off()
    ENA.duty_u16(0)
    ENB.duty_u16(0)

def izquierda():
    IN1.value(0); IN2.value(1)
    IN3.value(1); IN4.value(0)
    ENA.duty_u16(VELOCIDAD // 2)
    ENB.duty_u16(VELOCIDAD)

def derecha():
    IN1.value(1); IN2.value(0)
    IN3.value(0); IN4.value(1)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD // 2)

def At_izquierda():
    IN1.value(1); IN2.value(0)
    IN3.value(0); IN4.value(1)
    ENA.duty_u16(VELOCIDAD // 2)
    ENB.duty_u16(VELOCIDAD)

def At_derecha():
    IN1.value(0); IN2.value(1)
    IN3.value(1); IN4.value(0)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD // 2)


while True:
    cmd = sys.stdin.read(1)
    if not cmd:
        continue
    cmd = cmd.upper()
    if cmd == "F":
        adelante()
    elif cmd == "B":
        atras()
    elif cmd == "S":
        parar()
    elif cmd == "L":
        izquierda()
    elif cmd == "R":
        derecha()
    elif cmd == "BL":
        At_izquierda()
    elif cmd == "BR":
        At_derecha()


