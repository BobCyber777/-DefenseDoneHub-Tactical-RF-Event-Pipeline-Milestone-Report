class ConfidenceEngine:

    def calculate(self, entity):

        score = 0

        if entity.device_id:
            score += 40

        if entity.rf_signature:
            score += 20

        if len(entity.history) > 5:
            score += 20

        if entity.movement_pattern:
            score += 20

        return min(score, 100)
