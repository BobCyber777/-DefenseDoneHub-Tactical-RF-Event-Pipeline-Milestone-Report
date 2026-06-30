import asyncio
import logging
from modules.core.states import SystemState

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [STATE] - %(levelname)s - %(message)s')

class StateEngine:
    def __init__(self, payload_bridge=None):
        self.current_state = SystemState.INIT
        self.payload_bridge = payload_bridge
        
        # Define allowed linear transitions to prevent erratic behavior
        self._allowed_transitions = {
            SystemState.INIT: [SystemState.STANDBY, SystemState.FAILSAFE],
            SystemState.STANDBY: [SystemState.TRANSIT, SystemState.FAILSAFE],
            SystemState.TRANSIT: [SystemState.ACTIVE_OP, SystemState.RETURNING, SystemState.FAILSAFE],
            SystemState.ACTIVE_OP: [SystemState.TRANSIT, SystemState.RETURNING, SystemState.FAILSAFE],
            SystemState.RETURNING: [SystemState.STANDBY, SystemState.FAILSAFE],
            SystemState.FAILSAFE: [SystemState.STANDBY]  # Can only exit failsafe via explicit reset
        }

    async def transition_to(self, new_state: SystemState):
        """Safely transitions the system to a new state and manages payloads."""
        if new_state == self.current_state:
            return

        # Global override: Any state can transition to FAILSAFE
        if new_state == SystemState.FAILSAFE or new_state in self._allowed_transitions[self.current_state]:
            logging.info(f"Transitioning from {self.current_state.name} ──► {new_state.name}")
            
            old_state = self.current_state
            self.current_state = new_state
            
            # Execute state-change side effects
            await self._handle_state_change(old_state, new_state)
        else:
            logging.error(f"REJECTED: Invalid state transition attempted: {self.current_state.name} ──► {new_state.name}")

    async def _handle_state_change(self, old_state: SystemState, new_state: SystemState):
        """Internal hooks to control hardware/payloads based on state transitions."""
        
        # Entering ACTIVE_OP: Spin up the isolated payload environment
        if new_state == SystemState.ACTIVE_OP:
            logging.warning("Target geofence breached. Activating specialized payload bridge...")
            if self.payload_bridge:
                await self.payload_bridge.start_subsystem()

        # Exiting ACTIVE_OP or hitting FAILSAFE: Instantly kill secondary environments
        if old_state == SystemState.ACTIVE_OP or new_state == SystemState.FAILSAFE:
            if new_state == SystemState.FAILSAFE or new_state == SystemState.RETURNING:
                logging.warning("Exiting operational area or Failsafe triggered! Terminating payload immediately.")
                if self.payload_bridge:
                    await self.payload_bridge.stop_subsystem()
