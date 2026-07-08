from .base import BaseSensor


class RadarSensor(BaseSensor):

    name = "Radar"

    def connect(self):
        pass

    def read(self):
        return {
            "range": 152.4,
            "velocity": 13.8,
            "bearing": 214
        }

    def disconnect(self):
        pass
