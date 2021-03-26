import network
import socket
from machine import Pin
from time import sleep
import _thread

class Networking:
    
    def __init__(self):
        self.led = Pin(2,Pin.OUT)
        
        self.wifi_tcp = network.WLAN(network.STA_IF)
        self.wifi_ssid = 'AntiGrum'
        self.wifi_password = '1Kappeee'
        
        self.server_port = 50000
        self.socket = None
        self.address = None
        
        self.start_wifi()
        self.init_socket()
        self.listen()
        
    def start_wifi(self):
        if not self.wifi_tcp.isconnected():
            print('connecting to network...')
            self.wifi_tcp.active(True)
            self.wifi_tcp.connect(self.wifi_ssid, self.wifi_password)
            while not self.wifi_tcp.isconnected():
                pass
        print('network config:', self.wifi_tcp.ifconfig())

    def init_socket(self):
        self.address = socket.getaddrinfo('0.0.0.0', self.server_port)[0][-1]
        self.socket = socket.socket()
        self.socket.bi1nd(self.address)
        
    def listen_socket(self):
        while True:
            self.socket.listen(1)
            cl, self.address = self.socket.accept()
            print('client connected from', self.address)
            cl_file = cl.makefile('rwb', 0)
            line = str(cl_file.readline(), 'utf8')
            line = line.replace('\n', '')
            print(line)
            
            if line == 'toggle':
                self.led.value(not self.led.value())
            cl.close()
            
    def listen(self):
        _thread.start_new_thread(self.listen_socket, ())