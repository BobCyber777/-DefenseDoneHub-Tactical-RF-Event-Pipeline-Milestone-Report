import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [PAYLOAD] - %(levelname)s - %(message)s')

class PayloadBridge:
    def __init__(self):
        self._current_process = None
        self._monitor_task = None

    async def start_subsystem(self, tool_name: str = "generic_monitor"):
        """
        Spins up a designated analysis tool or containerized payload environment.
        Ensures only one operational tool runs at any given time.
        """
        if self._current_process and self._current_process.returncode is None:
            logging.warning("An analysis process is already running. Aborting duplicate spawn.")
            return

        logging.info(f"Initializing isolated environment for tool: {tool_name}")
        
        try:
            # Operational Guard: We run the process asynchronously using system-level boundaries.
            # Replace ['sleep', '60'] with your specific container execution or binary path, e.g., ['podman', 'run', ...]
            self._current_process = await asyncio.create_subprocess_exec(
                'sleep', '60',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Start the resource/timeout monitor thread
            self._monitor_task = asyncio.create_task(self._enforce_safety_limits(timeout_seconds=30))
            logging.info(f"Subsystem process started successfully (PID: {self._current_process.pid})")

        except Exception as e:
            logging.error(f"Failed to initialize payload subsystem: {str(e)}")

    async def stop_subsystem(self):
        """Forcibly terminates the running payload environment during a state transition or failsafe."""
        if self._monitor_task:
            self._monitor_task.cancel()

        if self._current_process and self._current_process.returncode is None:
            logging.warning(f"Terminating active payload process (PID: {self._current_process.pid})...")
            try:
                self._current_process.terminate()
                # Give it a moment to clean up gracefully, otherwise kill it
                await asyncio.wait_for(self._current_process.wait(), timeout=2.0)
                logging.info("Payload process terminated safely.")
            except asyncio.TimeoutError:
                logging.error("Process refused to terminate gracefully. Issuing SIGKILL.")
                self._current_process.kill()
                await self._current_process.wait()
        else:
            logging.info("No active payload processes detected during teardown request.")

    async def _enforce_safety_limits(self, timeout_seconds: int):
        """Monitors execution duration to ensure the payload does not overrun flight constraints."""
        try:
            await asyncio.sleep(timeout_seconds)
            if self._current_process and self._current_process.returncode is None:
                logging.error(f"Payload process exceeded safe runtime threshold ({timeout_seconds}s). Enforcing automatic safety cutoff.")
                await self.stop_subsystem()
        except asyncio.CancelledError:
            # Monitor was canceled cleanly because the process finished or was stopped by the state machine
            pass
