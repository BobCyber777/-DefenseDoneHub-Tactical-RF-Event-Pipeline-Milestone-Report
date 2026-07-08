class SensorManager:

    def __init__(self):
        self.sensors = []

    def register(self, sensor):
        self.sensors.append(sensor)

    def collect(self):
        events = []

        for sensor in self.sensors:
            events.append(sensor.read())

        return events
