import json
import asyncio
from asgiref.sync import async_to_sync
from channels.generic.websocket import SyncConsumer
import channels.layers



from .tail import Tail

GROUP_NAME = "logfile"

def get_updates():
    tail = Tail('../logfile.txt')
    tail.register_callback(broadcase_updates)
    tail.follow()

def broadcase_updates(line):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        GROUP_NAME, 
        {
            "type": 'push_updates',
            "text": line,
        }
        )


class LogConsumer(SyncConsumer):
    

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

        self.send({
            "type": "websocket.send",
            "text": self.first_10_lines_of_log()
        })
        async_to_sync(self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name,
        )

        if self.channel_layer.receive_count == 1:
            get_updates()


    def websocket_disconnect(self, close_code):

        print(close_code)
        async_to_sync(self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name,
        )
    

    def first_10_lines_of_log(self):
        
        f = open('../logfile.txt', 'r')
        lines = f.readlines()
        return '\n'.join(lines[-10:] if len(lines) > 10 else lines)


    def websocket_receive(self, event):
        print(event)

    def push_updates(self, event):
        print(event)
        print("events are reaching here")
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
