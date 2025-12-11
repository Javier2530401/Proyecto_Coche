python -m esptool --chip esp32 --port COM4 erase_flash 

python -m esptool --chip esp32 --port COM4 --baud 460800 write_flash -z 0x1000 upython-v1.26.1.bin

ampy --port COM4 put src\main.py main.py

ampy --port COM4 ls

