from machine import Pin, PWM, Timer
import bluetooth
import time

# ================== BLE UART ==================
_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)

_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX))

ble = bluetooth.BLE()
ble.active(True)

connections = set()
rx_buffer = []

def ble_irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("Conectado")
        connections.add(data[0])
    elif event == _IRQ_CENTRAL_DISCONNECT:
        print("Desconectado")
        connections.remove(data[0])
        advertise()
    elif event == _IRQ_GATTS_WRITE:
        msg = ble.gatts_read(rx_handle)
        try:
            rx_buffer.append(msg.decode().strip().upper())
        except:
            print("Error al decodificar mensaje")

ble.irq(ble_irq)

((tx_handle, rx_handle),) = ble.gatts_register_services((_UART_SERVICE,))

def advertise():
    name = "ESP32-CAR"
    adv_data = bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name.encode()
    ble.gap_advertise(100_000, adv_data=adv_data)
    print("Anunciando BLE:", name)

advertise()

# ================== MOTORES L298N ==================
ENA = PWM(Pin(14), freq=1000)
IN1 = Pin(12, Pin.OUT)
IN2 = Pin(13, Pin.OUT)

ENB = PWM(Pin(27), freq=1000)
IN3 = Pin(25, Pin.OUT)
IN4 = Pin(26, Pin.OUT)

VELOCIDAD = 30000  # puedes ajustar entre 0-65535

def avanzar():
    IN1.value(0); IN2.value(1)
    IN3.value(1); IN4.value(0)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD)

def retroceder():
    IN1.value(1); IN2.value(0)
    IN3.value(0); IN4.value(1)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD)

def izquierda():
    IN1.value(1); IN2.value(0)
    IN3.value(1); IN4.value(0)
    ENA.duty_u16(VELOCIDAD // 2)
    ENB.duty_u16(VELOCIDAD)

def derecha():
    IN1.value(0); IN2.value(1)
    IN3.value(0); IN4.value(1)
    ENA.duty_u16(VELOCIDAD)
    ENB.duty_u16(VELOCIDAD // 2)

def detener():
    ENA.duty_u16(0)
    ENB.duty_u16(0)
    IN1.value(0); IN2.value(0)
    IN3.value(0); IN4.value(0)

# ================== Timer ping (opcional) ==================


# ================== Loop principal ==================
current_cmd = ""

while True:
    if rx_buffer:
        cmd = rx_buffer.pop(0)
        print("Comando recibido:", cmd)

        if cmd != current_cmd:
            detener()
            current_cmd = cmd

        if cmd == "W":
            avanzar()
        elif cmd == "S":
            retroceder()
        elif cmd == "A":
            izquierda()
        elif cmd == "D":
            derecha()
        elif cmd == "X":
            detener()
        else:
            print("Comando no reconocido:", cmd)

    time.sleep(0.05)