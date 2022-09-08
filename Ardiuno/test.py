import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9800, timeout=1)
time.sleep(2)

while True:
    ser.writelines(b'H')   # send a byte
    time.sleep(0.2)        # wait 0.5 seconds
    ser.writelines(b'L')   # send a byte
    time.sleep(0.3)

ser.close()
