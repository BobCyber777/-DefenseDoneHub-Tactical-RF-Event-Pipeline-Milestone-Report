import asyncio
from modules.signal_capture.receiver import SignalCaptureModule
from modules.analysis.engine import VulnerabilityAnalyzer
from modules.injection_engine.transmitter import PacketInjectionEngine

async def main():
    # 1. Initialize communication queues and core modules
    shared_queue = asyncio.Queue(maxsize=100)
    
    capture_mod = SignalCaptureModule(shared_queue)
    analyzer_mod = VulnerabilityAnalyzer()
    injector_mod = PacketInjectionEngine(interface="wlan0mon")

    print("\n========================================================")
    print("--- INITIATING CLOSED-LOOP SIGNAL ASSESSMENT MATRIX ---")
    print("========================================================\n")
    
    # 2. Spin up the background capture thread
    await capture_mod.start_capture("wlan0mon")

    # 3. Process the stream and trigger active validation loops
    try:
        for _ in range(5):  # Run a 5-step sample sequence for validation
            frame = await shared_queue.get()
            
            # Execute real-time parsing
            findings = await analyzer_mod.analyze_frame(frame)
            
            for finding in findings:
                print(f"⚠️  [VULNERABILITY DETECTED] [{finding['severity']}] {finding['type']}")
                print(f"   Detail: {finding['description']}")
                print(f"   Fix:    {finding['remediation']}")
                
                # Closed-Loop Interaction: Trigger active verification frames
                await injector_mod.inject_verification_frame(finding['type'])
                
            shared_queue.task_done()
            await asyncio.sleep(0.1)
            
    finally:
        # 4. Clean up interfaces smoothly
        await capture_mod.stop_capture()
        print("--- ASSESSMENT SEQUENCE CONCLUDED ---")

if __name__ == "__main__":
    asyncio.run(main())
