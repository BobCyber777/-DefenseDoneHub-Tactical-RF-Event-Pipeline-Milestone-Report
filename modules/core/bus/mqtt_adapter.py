import json
import paho.mqtt.client as mqtt
from modules.core.bus.event_bus import BaseEventBus


class MQTTEventBus(BaseEventBus):

    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker, port, 60)

    def publish(self, topic: str, event):
        self.client.publish(topic, json.dumps(event.to_dict()))

    def subscribe(self, topic: str, handler):

        def on_message(client, userdata, msg):
            payload = json.loads(msg.payload.decode())
            handler(payload)

        self.client.subscribe(topic)
        self.client.on_message = on_message
        self.client.loop_start()
