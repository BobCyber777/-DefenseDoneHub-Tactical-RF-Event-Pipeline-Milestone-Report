"""
Controlled Injection Layer
Main gatekeeper for all injection actions.
"""

import asyncio

from .policies import PolicyEngine
from .safety import SafetyEngine
from .auth import InjectionAuthorization


class InjectionController:

    def __init__(self, injector):

        self.injector = injector

        self.policy_engine = PolicyEngine()
        self.safety_engine = SafetyEngine()
        self.auth = InjectionAuthorization()

        self.enabled = True

    async def execute(self, event, mission_state):

        if not self.enabled:
            print("[INJECTION BLOCKED] System disabled")
            return False

        # 1. Authorization check (mission-level permission)
        if not self.auth.is_allowed(mission_state, event):
            print("[INJECTION BLOCKED] Authorization failed")
            return False

        # 2. Policy check (rule-based permission)
        if not self.policy_engine.is_allowed(mission_state, event):
            print("[INJECTION BLOCKED] Policy denied")
            return False

        # 3. Safety constraints (rate limiting / protection)
        if not self.safety_engine.allow():
            print("[INJECTION BLOCKED] Safety limit reached")
            return False

        # 4. EXECUTE INJECTION (final action)
        await self.injector.inject_verification_frame(event.event_type)

        # 5. Register usage
        self.safety_engine.record()

        print(f"[INJECTION EXECUTED] {event.event_type}")

        return True
