from abc import ABC, abstractmethod


class BaseSensor(ABC):
    """
    Base class for all DefenseDoneHub sensors.
    """

    name = "sensor"

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read(self):
        """
        Return normalized sensor data.
        """
        pass

    @abstractmethod
    def disconnect(self):
        pass
