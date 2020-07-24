import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time

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
        for i in range(10):
            text = f"test send {i}"
            self.send(json.dumps({
                "text": text
            }))
            time.sleep(2)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "Tempclients",
            self.channel_name
        )

status = 0
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
            print("Light is on")
            async_to_sync(self.channel_layer.group_send)(
                "LightClients",
                {
                    "type": "lightStt",
                    "status": status
                }
            )
        elif (status == "off"):
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
            print("Light is blinking") 
            time.sleep(10)
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
