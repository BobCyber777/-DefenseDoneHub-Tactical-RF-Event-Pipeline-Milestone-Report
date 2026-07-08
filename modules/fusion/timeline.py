class Timeline:

    def add(self, entity, observation):

        entity.history.append({
            "timestamp": observation["timestamp"],
            "event": observation,
        })
