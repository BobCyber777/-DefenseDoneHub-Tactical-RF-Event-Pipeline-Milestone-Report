from enum import Enum, auto

class SystemState(Enum):
    INIT = auto()            # System self-check and hardware initialization
    STANDBY = auto()         # Armed or disarmed, awaiting mission/target GPS
    TRANSIT = auto()         # In flight toward target; secondary payloads dormant
    ACTIVE_OP = auto()       # Inside geofence; payload bridge running specialized tasks
    RETURNING = auto()       # Mission complete or low battery; heading home
    FAILSAFE = auto()        # Emergency state; immediate payload shutdown, RTB or land
