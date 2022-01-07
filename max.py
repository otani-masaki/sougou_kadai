import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.PilotingSettings import MaxAltitude, MaxDistance, MaxTilt
from olympe.messages.ardrone3.PilotingSettingsState import MaxAltitudeChanged, MaxTiltChanged

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")


def test_moveby2():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()

    # assert drone(
    #     MaxAltitude(current=2)
    #     >> MaxAltitudeChanged(current=2.0, min=0.5, max=5.0)
    # ).wait().success()
    drone(MaxTilt(1)
     >> MaxTiltChanged(1,1,1)
    ).wait().success()
    assert drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    assert drone(
        moveBy(5, 0, -10, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    assert drone(Landing()).wait().success()
    drone.disconnect()


if __name__ == "__main__":
    test_moveby2()
