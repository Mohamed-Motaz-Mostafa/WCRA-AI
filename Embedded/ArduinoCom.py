import serial

def getArduinoResponse():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    while not ser.in_waiting:
        continue
    line = ser.readline().decode('utf-8').rstrip()
    return line 
