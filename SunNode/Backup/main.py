import network
import socket
from machine import Pin
from time import sleep

led = Pin(2,Pin.OUT)

#Wifi connection
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('AntiGrum', '1Kappeee')
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

#Server setup
import socket
addr = socket.getaddrinfo('0.0.0.0', 50000)[0][-1]

s = socket.socket()
s.bind(addr)

print('listening on', addr)

while True:
    try:
        s.listen(1)
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        line = str(cl_file.readline(), 'utf8')
        line = line.replace('\n', '')
        print(line)
        
        if line == "toggle":
            led.value(not led.value())
        cl.close()
    except OSError as error:
        print("OS error: {0}".format(error))
        cl.close()
