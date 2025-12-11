# MATERIA
## METODOLOGIAS DE LA PROGRAMACION.

# PROFESOR
## M.C CARLOS ANTONIO TOVAR 

# ALUMNO
## Javier de Jesús Camacho Guevara

# Materiales que utilizamos

### - ESP-32
### - L298N
### - 4 Moto-reductores
### - Base del carrito
### - Porta Pilas
### - Interuptor
### - 4 Ruedas

# Código 1
### ¿Que ase este codigo?
### Este codigo es el que esta dentro de la esp32 es decir es el que permite el funcionamiento de el cochesito leyendo los comandos de que son mandados por el mando que resibe como letras ( F, B, L, R Y S ).

```python
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
    
```

# Código 2
### ¿Que ase este codigo?
### Este programa permite controlar un robot mediante un joystick conectado a una computadora. Los movimientos del joystick se leen y se envían como comandos al ESP32 a través de la conexión serial ( F, B, L, R Y S ). El robot puede moverse hacia adelante, atrás, girar a la izquierda o derecha, y detenerse automáticamente cuando el joystick está en reposo.

```python
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
            esp32.write(b"F") 
        elif y_axis > 0.5:
            esp32.write(b"B")
        elif x_axis < -0.5:
            esp32.write(b"L")  
        elif x_axis > 0.5:
            esp32.write(b"R")  
        else:
            esp32.write(b"S")  
        time.sleep(0.1)

except KeyboardInterrupt:
    esp32.write(b"S")
    esp32.close()
    print("Programa finalizado")
```

# ENTRADAS
| Variable     | Tipo       | Fuente                          | Descripción                                                                             |
| ------------ | ---------- | ------------------------------- | --------------------------------------------------------------------------------------- |
| `joystick`   | `Joystick` | `pygame.joystick.Joystick(0)`   | Objeto que representa el joystick conectado.                                            |
| `x_axis`     | `float`    | `joystick.get_axis(0)`          | Valor del eje X del joystick (-1.0 a 1.0), controla los movimientos laterales.              |
| `y_axis`     | `float`    | `joystick.get_axis(1)`          | Valor del eje Y del joystick (-1.0 a 1.0), controla los movimiento de adelante y atrás.       |
| `esp32`      | `Serial`   | `serial.Serial('COM4', 115200)` | Objeto de comunicación serial con el ESP32.                                             |
| `cmd`        | `bytes`    | Procesamiento interno           | Comando que se envía al ESP32 según la posición del joystick (`F`, `B`, `L`, `R`, `S`). |
| `time.sleep` | `float`    | `time`                          | Retardo entre envíos de comandos para evitar saturar el serial.                         |

# Motores

| Variable / Función | Función / Salida                                                                     |
| ------------------ | ------------------------------------------------------------------------------------ |
| `ENA`     | Objeto PWM que controla la velocidad del Motor A mediante `duty_u16`.                |
| `ENB`    | Objeto PWM que controla la velocidad del Motor B mediante `duty_u16`.                |
| `IN1`       | Pin de dirección del Motor A.                                                        |
| `IN2`       | Pin de dirección del Motor A.                                                        |
| `IN3`      | Pin de dirección del Motor B.                                                        |
| `IN4`       | Pin de dirección del Motor B.                                                        |
| `VELOCIDAD`        | Valor de velocidad definido (0–65535) para ambos motores.                            |
| `adelante()`       | Hace que ambos motores giren hacia adelante.                                         |
| `atras()`          | Hace que ambos motores giren hacia atrás.                                            |
| `parar()`          | Detiene ambos motores.                                                               |
| `izquierda()`      | Gira el robot hacia la izquierda.                |
| `derecha()`        | Gira el robot hacia la derecha.                  |
| `cmd`              | Comando recibido por consola (`F`, `B`, `L`, `R`, `S`) para controlar el movimiento. |

# VALIDACONES
### - if not cmd: continue Valida que se haya ingresado un comando desde la consola si no hay comando, simplemente continúa el ciclo sin ejecutar nada.
### cmd.upper(): Convierte el comando a mayúscula, permitiendo que se escriba f o F y funcione igual.
### Condicional if/elif: Solo ejecuta una función si el comando coincide con "F", "B", "S", "L" o "R" cualquira que no sea ese no hace nada.

# RESULTADOS
### El proyecto funciono con brios contratiempos pero funciono cumplio con lo que pidio pero pudo ser mejor.
### El funcionamiento es sencillo el coche est conectado a la pc por un cable y desde la pc se mandan comandos mediante un Joystick conectado por bluetooth a la pc permitiendo su funcionamieno.

# CONTRATIEMPOS Y OBSERVACIONES
### - Siempre comprobar cuanta es el voltaje nesesario para el funcionamiento de los componentes.
### - Siempre comprobar que tengas el aveinte activo.

# CONCLUSION
### En conclusión, durante este proyecto aprendí a manejar una ESP32, incluyendo cómo conectarla a la computadora, subirle archivos y borrar su memoria flash. Además, comprendí cómo se comportan los motores al ser controlados y cómo interactúan con el microcontrolador, lo que me permitió mejorar mis conocimientos prácticos y control de dispositivos electrónicos.

### Por ultimo aprndi que es mejor tener un plan desde el inicio y no comenzar un proyecto sin un plan ya planeado balga la redundancia.
