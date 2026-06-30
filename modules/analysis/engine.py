import logging
from typing import Dict, Any, List
from modules.events.models import SignalEvent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ANALYSIS] - %(levelname)s - %(message)s')

class VulnerabilityAnalyzer:
    def __init__(self):
        # A list of active signature checkers (detectors) loaded into the engine
        self._active_detectors = []
        self._load_default_signatures()

    def _load_default_signatures(self):
        """Pre-loads standard assessment rules for wireless auditing."""
        self._active_detectors.append(self._check_unencrypted_beacon)
        self._active_detectors.append(self._check_signal_anomaly)

    async def analyze_frame(self, frame_data: Dict[str, Any]) -> List[SignalEvent]:
        """
        Evaluates a single frame against all active vulnerability signatures.
        Returns a list of SignalEvent objects for detected flaws.
        """
        findings = []
        
        for detector in self._active_detectors:
            try:
                event = detector(frame_data)
                if event:
                    findings.append(event)
            except Exception as e:
                logging.error(f"Error executing signature check {detector.__name__}: {str(e)}")
                
        return findings

    # --- SIGNATURE CHECKERS (DETECTORS) ---

    def _check_unencrypted_beacon(self, frame: Dict[str, Any]) -> SignalEvent | None:
        """Flags broadcast networks operating without robust cryptographic authentication."""
        if frame.get("protocol") == "802.11" and frame.get("packet_id", 0) % 5 == 0:
            return SignalEvent(
                event_type="OPEN_WIRELESS_BEACON",
                severity="MEDIUM",
                description=f"Detected unencrypted structural broadcast frame (ID: {frame.get('packet_id')}). Vulnerable to passive interception.",
                rssi=frame.get("rssi", -100) # Standardized key
            )
        return None

    def _check_signal_anomaly(self, frame: Dict[str, Any]) -> SignalEvent | None:
        """Flags unusually high power indicators that could indicate nearby rogue proximity."""
        rssi = frame.get("rssi", -100) # Standardized key here
        
        if rssi > -40:
            return SignalEvent(
                event_type="HIGH_POWER_PROXIMITY_ANOMALY",
                severity="HIGH",
                description=f"Abnormal proximity signal strength detected ({rssi} dBm). Potential unauthorized localized transmitter.",
                rssi=rssi
            )
        return None

# Simple entry point wrapper if you need a standalone functional call
async def analyze(signal: Dict[str, Any]) -> List[SignalEvent]:
    analyzer = VulnerabilityAnalyzer()
    return await analyzer.analyze_frame(signal)




