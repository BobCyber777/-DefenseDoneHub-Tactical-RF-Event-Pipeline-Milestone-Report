import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Digging straight into your existing modules
from modules.signal_capture.receiver import SignalCaptureModule
from modules.analysis.engine import VulnerabilityAnalyzer
from modules.injection_engine.transmitter import PacketInjectionEngine

class AlertStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # 1. Setup the exact same asynchronous pipeline from main.py
        self.shared_queue = asyncio.Queue(maxsize=100)
        self.capture_mod = SignalCaptureModule(self.shared_queue)
        self.analyzer_mod = VulnerabilityAnalyzer()
        self.injector_mod = PacketInjectionEngine(interface="wlan0mon")
        
        # 2. Spin up the hardware interface capture stream
        await self.capture_mod.start_capture("wlan0mon")
        
        # 3. Keep the background analyzer running concurrently inside the socket
        self.processing_task = asyncio.create_task(self._stream_analysis_loop())

    async def disconnect(self, close_code):
        # Clean shutdown: kill tasks and return antenna to a safe state
        if hasattr(self, 'processing_task'):
            self.processing_task.cancel()
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
            pass




