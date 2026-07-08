class EntityMatcher:

    def __init__(self, graph):
        self.graph = graph

    def match(self, observation):

        for entity in self.graph.entities.values():

            if entity.device_id == observation.get("device_id"):
                return entity

        return self.graph.create_entity(observation)
