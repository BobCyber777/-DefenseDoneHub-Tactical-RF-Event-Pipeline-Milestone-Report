from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DroneEntity:

    entity_id: str

    device_id: str | None = None

    rf_signature: dict = field(default_factory=dict)

    movement_pattern: list = field(default_factory=list)

    first_seen: datetime | None = None

    last_seen: datetime | None = None

    history: list = field(default_factory=list)

    confidence: float = 0.0
