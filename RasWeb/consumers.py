import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time

class TempConsumer(WebsocketConsumer):
    def connect(self):
        print("A client connected to temp socket")
        self.accept()
        for i in range (10):
            self.send(json.dumps({
                "text": f"Hello{i}"    
            }))
            time.sleep(1)
    def disconnect(self):
        pass
status = 0
class LightConsumer(WebsocketConsumer):
    def connect(self):
        global status
        print("A client connected to light socket")
        async_to_sync(self.channel_layer.group_add)(
            "clients",
            self.channel_name
        )
        self.accept()
        if (status != 0):
            self.send(json.dumps({
                "status": status
            }))
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "clients",
            self.channel_name
        )
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json["status"]
        if (status == "on"):
            print("Light is on")
            async_to_sync(self.channel_layer.group_send)(
                "clients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
        elif (status == "off"):
            print("Light is off")
            async_to_sync(self.channel_layer.group_send)(
                "clients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
        elif (status == "blink"):
            async_to_sync(self.channel_layer.group_send)(
                "clients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
            print("Light is blinking") 
            time.sleep(5)
            async_to_sync(self.channel_layer.group_send)(
                "clients",
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