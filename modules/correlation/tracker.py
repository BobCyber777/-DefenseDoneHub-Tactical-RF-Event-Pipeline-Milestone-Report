"""
Correlation Engine

Entity tracker (in-memory store)
"""

from typing import Dict, Optional
from .entities import Entity


class EntityTracker:

    def __init__(self):
        self.entities: Dict[str, Entity] = {}

    def get_or_create(self, entity_id: str, event, fingerprint: str):

        if entity_id not in self.entities:
            self.entities[entity_id] = Entity(entity_id=entity_id)

        entity = self.entities[entity_id]
        entity.update(event, fingerprint)

        return entity

    def all(self):
        return list(self.entities.values())

    def get(self, entity_id) -> Optional[Entity]:
        return self.entities.get(entity_id)
