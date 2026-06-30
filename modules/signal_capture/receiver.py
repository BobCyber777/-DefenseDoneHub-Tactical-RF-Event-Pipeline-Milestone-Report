import asyncio
import logging
logging.basicConfig(level=logging.INFO)
class SignalCaptureModule:
    def __init__(self, q):
        self.q = q
        self._active = False
    async def start_capture(self, i):
        self._active = True
        self._t = asyncio.create_task(self._read())
    async def stop_capture(self):
        self._active = False
        if hasattr(self, '_t'): self._t.cancel()
    async def _read(self):
        c = 0
        while self._active:
            await asyncio.sleep(0.5)
            c += 1
            await self.q.put({'packet_id': c, 'signal_strength_dbm': -35 if c % 3 == 0 else -65, 'protocol': '802.11'})
