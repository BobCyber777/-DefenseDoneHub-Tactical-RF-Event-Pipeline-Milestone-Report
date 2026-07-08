import json
from kafka import KafkaProducer
from modules.core.bus.event_bus import BaseEventBus


class KafkaEventBus(BaseEventBus):

    def __init__(self, bootstrap_servers="localhost:9092"):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish(self, topic: str, event):
        self.producer.send(topic, event.to_dict())
        self.producer.flush()

    def subscribe(self, topic: str, handler):
        raise NotImplementedError("Use Kafka consumer service separately")
