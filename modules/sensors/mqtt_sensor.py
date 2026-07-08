from .base import BaseSensor


class MQTTSensor(BaseSensor):

    name = "MQTT"

    def connect(self):
        pass

    def read(self):
        return {
            "topic": "drone/telemetry",
            "payload": {}
        }

    def disconnect(self):
        pass
