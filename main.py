import asyncio

from modules.signal_capture.receiver import SignalCaptureModule
from modules.analysis.engine import VulnerabilityAnalyzer
from modules.injection_engine.transmitter import PacketInjectionEngine

from modules.core.bus.event_bus import EventBus
from modules.core.bus.django_adapter import django_store_event
from modules.events.schema import SecurityEvent

# ✅ ADD RULE ENGINE
from modules.rules.subscriber import RuleSubscriber


async def main():

    # 1. Core infrastructure
    shared_queue = asyncio.Queue(maxsize=100)
    bus = EventBus()

    print("\n========================================================")
    print("--- INITIATING CLOSED-LOOP SIGNAL ASSESSMENT MATRIX ---")
    print("========================================================\n")

    # 2. Attach subscribers (IMPORTANT ORDER DOES NOT MATTER)
    bus.subscribe(django_store_event)

    rule_subscriber = RuleSubscriber()
    bus.subscribe(rule_subscriber.handle)

    # 3. Modules
    capture_mod = SignalCaptureModule(shared_queue)
    analyzer_mod = VulnerabilityAnalyzer()
    injector_mod = PacketInjectionEngine(interface="wlan0mon")

    # 4. Start capture
    await capture_mod.start_capture("wlan0mon")

    try:
        for _ in range(5):

            frame = await shared_queue.get()

            findings = await analyzer_mod.analyze_frame(frame)

            for finding in findings:

                event_type = getattr(finding, "event_type", None)
                severity = getattr(finding, "severity", "UNKNOWN")
                description = getattr(finding, "description", "")
                rssi = getattr(finding, "rssi", None)

                print(f"⚠️  [VULNERABILITY DETECTED] [{severity}] {event_type}")
                print(f"   Detail: {description}")
                print(f"   Fix:    {getattr(finding, 'remediation', 'N/A')}")

                event = SecurityEvent(
                    event_type=event_type,
                    severity=severity,
                    description=description,
                    rssi=rssi,
                    source="wlan0mon"
                )

                # 5. Publish to full system
                await bus.publish(event)

                # 6. Injection (kept for now, but architecture warning)
                await injector_mod.inject_verification_frame(event_type)

            shared_queue.task_done()
            await asyncio.sleep(0.1)

    finally:
        await capture_mod.stop_capture()
        print("--- ASSESSMENT SEQUENCE CONCLUDED ---")


if __name__ == "__main__":
    asyncio.run(main())
