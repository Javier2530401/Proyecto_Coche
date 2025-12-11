import pygame
import serial
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No se detectó ningún joystick")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

esp32 = serial.Serial('COM4', 115200, timeout=0.1)  
time.sleep(2)

print("Control activo. Usa los sticks o botones para mover el coche")

try:
    while True:
        pygame.event.pump()  
        y_axis = joystick.get_axis(1)  
        x_axis = joystick.get_axis(0)  

        if y_axis < -0.5:
            esp32.write(b"F")  # Adelante
        elif y_axis > 0.5:
            esp32.write(b"B")  # Atrás
        elif x_axis < -0.5:
            esp32.write(b"L")  # Izquierda
        elif x_axis > 0.5:
            esp32.write(b"R")  # Derecha
        else:
            esp32.write(b"S")  # Parar si está en neutro
        time.sleep(0.1)

except KeyboardInterrupt:
    esp32.write(b"S")
    esp32.close()
    print("Programa finalizado")