import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time
import RPi.GPIO as GPIO 
import os
import glob

# Reading temperature from censor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#SocketIO implementation
class TempConsumer(WebsocketConsumer):
    def connect(self):
        print("A client connected to temp socket")
        async_to_sync(self.channel_layer.group_add)(
            "TempClients", 
            self.channel_name
        )
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            "TempClients",
            {
                "type": "temp",
            }
        )

    def temp(self, event):
        while True:
            tempC, tempF = read_temp()
            self.send(json.dumps({
                "tempC": "{:.2f}".format(tempC),
                "tempF": "{:.2f}".format(tempF)
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "Tempclients",
            self.channel_name
        )

status = 0
GPIO.warnings = False 
LED_PIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
class LightConsumer(WebsocketConsumer):
    def connect(self):
        global status
        print("A client connected to light socket")
        async_to_sync(self.channel_layer.group_add)(
            "LightClients",
            self.channel_name
        )
        self.accept()
        if (status != 0):
            print(status)
            self.send(json.dumps({
                "status": status
            }))
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "LightClients",
            self.channel_name
        )
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json["status"]
        if (status == "on"):
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("Light is on")
            async_to_sync(self.channel_layer.group_send)(
                "LightClients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
        elif (status == "off"):
            GPIO.output(LED_PIN, GPIO.LOW)
            print("Light is off")
            async_to_sync(self.channel_layer.group_send)(
                "LightClients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
        elif (status == "blink"):
            async_to_sync(self.channel_layer.group_send)(
                "LightClients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
            for i in range(10):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.5)
            print("Light blinked") 
            async_to_sync(self.channel_layer.group_send)(
                "LightClients",
                {
                    "type": "lightStt",
                    "status": "blink done"
                }
            )
    
    def lightStt(self, event):
        global status
        status = event['status']
        self.send(json.dumps({
            'status': status 
        }))