import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Importing existing modules
from modules.signal_capture.receiver import SignalCaptureModule
from modules.analysis.engine import VulnerabilityAnalyzer
from modules.injection_engine.transmitter import PacketInjectionEngine

class AlertStreamConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Accept the WebSocket connection first
        await self.accept()

        # 1. Setup the asynchronous pipeline
        self.shared_queue = asyncio.Queue(maxsize=100)
        self.capture_mod = SignalCaptureModule(self.shared_queue)
        self.analyzer_mod = VulnerabilityAnalyzer()
        self.injector_mod = PacketInjectionEngine(interface="wlan0mon")

        # 2. Spin up the hardware interface capture stream as a background task
        # (Using create_task ensures it runs concurrently without blocking the handshake)
        self.capture_task = asyncio.create_task(
            self.capture_mod.start_capture("wlan0mon")
        )

        # 3. Keep the background analyzer running concurrently inside the socket
        self.processing_task = asyncio.create_task(self._stream_analysis_loop())

    async def disconnect(self, close_code):
        # Clean shutdown: kill tasks and return interface to a safe state
        if hasattr(self, 'processing_task'):
            self.processing_task.cancel()
            
        if hasattr(self, 'capture_task'):
            self.capture_task.cancel()

        await self.capture_mod.stop_capture()

    async def _stream_analysis_loop(self):
        try:
            while True:
                # Pull raw data emitted by modules.signal_capture
                frame = await self.shared_queue.get()

                # Run evaluation via modules.analysis
                findings = await self.analyzer_mod.analyze_frame(frame)

                for finding in findings:
                    # Push alert properties down the WebSocket to the browser UI
                    await self.send(text_data=json.dumps({
                        'type': finding['type'],
                        'severity': finding['severity'],
                        'description': finding['description'],
                        'remediation': finding['remediation']
                    }))

                    # Run verification frame via modules.injection_engine
                    await self.injector_mod.inject_verification_frame(finding['type'])

                self.shared_queue.task_done()
        except asyncio.CancelledError:
            # Handle graceful cancellation when the WebSocket disconnects
            pass




