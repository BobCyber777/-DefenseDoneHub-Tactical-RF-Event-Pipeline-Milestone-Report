"""
Controlled Injection Layer
Policies define WHEN injection is allowed.
"""

from dataclasses import dataclass


@dataclass
class InjectionPolicy:
    """
    Defines a single rule for injection permission.
    """

    name: str
    allowed_states: list
    min_severity: str


class PolicyEngine:

    SEVERITY_LEVELS = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    def __init__(self):

        # Default system policies
        self.policies = [
            InjectionPolicy(
                name="defensive_only",
                allowed_states=["defensive", "lockdown"],
                min_severity="HIGH"
            ),

            InjectionPolicy(
                name="lockdown_override",
                allowed_states=["lockdown"],
                min_severity="MEDIUM"
            )
        ]

    def is_allowed(self, mission_state, alert):
        """
        Check if ANY policy allows injection.
        """

        alert_level = self.SEVERITY_LEVELS.get(alert.severity, 0)

        for policy in self.policies:

            if mission_state not in policy.allowed_states:
                continue

            if alert_level >= self.SEVERITY_LEVELS.get(policy.min_severity, 0):
                return True

        return False
