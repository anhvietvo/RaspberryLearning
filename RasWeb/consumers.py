import json
from channels.generic.websocket import WebsocketConsumer
import time

class WebConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        self.accept()
        for i in range (10):
            self.send(json.dumps({
                "type": "websocket.send",
                "text": f"Hello{i}"    
            }))
            time.sleep(1)
    def disconnect(self):
        pass