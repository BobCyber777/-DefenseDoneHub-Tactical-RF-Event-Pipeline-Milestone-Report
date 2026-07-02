"""
Controlled Injection Layer
Mission-level authorization gate.
"""

class InjectionAuthorization:

    def __init__(self):

        # Only these mission states can ever trigger injection
        self.allowed_states = {
            "DEFENSIVE",
            "LOCKDOWN"
        }

    def is_allowed(self, mission_state, event):
        """
        Mission-level permission check.
        """

        # Normalize state
        state = str(mission_state).upper()

        # 1. Block everything outside allowed mission states
        if state not in self.allowed_states:
            return False

        # 2. Basic severity floor (extra safety layer)
        severity = getattr(event, "severity", "LOW")

        if severity in ["LOW"]:
            return False

        # 3. Must have valid event type
        if not getattr(event, "event_type", None):
            return False

        return True
