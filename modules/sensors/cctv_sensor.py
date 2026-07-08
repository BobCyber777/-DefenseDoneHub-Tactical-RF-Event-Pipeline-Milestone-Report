from .base import BaseSensor


class CCTVSensor(BaseSensor):

    name = "CCTV"

    def connect(self):
        pass

    def read(self):
        return {
            "camera_id": "CAM-01",
            "status": "online",
            "frame": None
        }

    def disconnect(self):
        pass
