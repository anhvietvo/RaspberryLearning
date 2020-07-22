import json
from channels.generic.websocket import WebsocketConsumer

class WebConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        self.accept()
        self.send(json.dumps({
            "type": "websocket.send",
            "text": "Hello"    
        }))
    def disconnect(self):
        pass