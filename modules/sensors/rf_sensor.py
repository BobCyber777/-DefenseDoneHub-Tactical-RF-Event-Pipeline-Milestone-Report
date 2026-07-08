from .base import BaseSensor


class RFSensor(BaseSensor):

    name = "RF"

    def connect(self):
        print("Connecting RF receiver...")

    def read(self):
        return {
            "signal_strength": -47,
            "frequency": 2437,
            "protocol": "802.11"
        }

    def disconnect(self):
        print("RF disconnected.")
