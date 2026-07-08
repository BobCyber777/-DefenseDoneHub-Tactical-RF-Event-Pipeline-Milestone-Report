from .matcher import EntityMatcher
from .confidence import ConfidenceEngine


class FusionEngine:

    def __init__(self, graph):
        self.graph = graph
        self.matcher = EntityMatcher(graph)
        self.confidence = ConfidenceEngine()

    def process(self, observation):

        entity = self.matcher.match(observation)

        entity.history.append(observation)

        entity.confidence = self.confidence.calculate(entity)

        return entity
