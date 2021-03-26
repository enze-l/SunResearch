import network
import socket
from machine import Pin
from time import sleep
import _thread

class Networking:
    
    def __init__(self, lightsensor):
        self.lightsensor = lightsensor
        
        self.led = Pin(2,Pin.OUT)
        
        self.wifi_tcp = network.WLAN(network.STA_IF)
        self.wifi_ssid = None
        self.wifi_password = None
        self.read_initials()
        
        self.server_port = 50000
        self.socket = None
        self.address = None
        
        self.start_networking()
    
    # Expecting wifi login information to be stored in files 'SSID'
    # and 'PASSWORD'
    def read_initials(self):
        fileSsid = open('SSID', 'r')
        filePassw = open('PASSWORD', 'r')
        self.wifi_ssid = str(fileSsid.readline(), 'utf8')
        self.wifi_password = str(filePassw.readline(), 'utf8')
        
    def start_networking(self):
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
        self.socket.bind(self.address)
        
    def listen(self):
        _thread.start_new_thread(self.listen_socket, ())
        
    def listen_socket(self):
        while True:
            self.socket.listen(1)
            cl, self.address = self.socket.accept()
            print('client connected from', self.address)
            cl_file = cl.makefile('rwb', 0)
            line = str(cl_file.readline(), 'utf8')
            line = line.replace('\n', '')
            print(line)
            self.execute_command(line, cl)
            cl.close()
        
    def execute_command(self, line, cl):
        if line == 'toggle':
            self.led.value(not self.led.value())
        if line == 'automation':
            print(self.lightsensor.get_data())
            cl.send(self.lightsensor.get_data_string() + '\n')
            #cl.send('Hello! \n')
