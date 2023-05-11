import pyfirmata
import time
import requests
import json
import serial.tools.list_ports

import config

arduino_digital_pin = config.arduino_digital_pin

def find_arduino_com_port():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description or 'CH340' in p.description or 'FTDI' in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        print('Multiple Arduinos found - using the first one')
    return arduino_ports[0]

def main():
    try:
        query_string = dict(key=config.Authorization)
        r = requests.request('GET', config.URL, params=query_string)
        count = int(r.content)
    except:
        print("Error: while fetching data.")
        print("Error: content is", r.content)
        count = 0
    if count>0: # have messages
        print(f"There are {count} messages")
        COMport = find_arduino_com_port()
        print(f"Arduino is connected on port: {COMport}")
        board = pyfirmata.Arduino(COMport, baudrate=57600)
        board.digital[arduino_digital_pin].mode = pyfirmata.PWM
        for i in range(3):
            board.digital[arduino_digital_pin].write(100)
            time.sleep(1)
            board.digital[arduino_digital_pin].write(0)
            time.sleep(1)
        board.exit()

if __name__ == '__main__':
    main()
