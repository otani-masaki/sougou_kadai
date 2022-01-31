import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing

from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged

# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")


def test_takeoff():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()

    # assert drone(
    #     FlyingStateChanged(state="hovering", _policy="check")
    #     | FlyingStateChanged(state="flying", _policy="check")
    #     | (
    #         GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
    #         >> (
    #             TakeOff(_no_expect=True)
    #             & FlyingStateChanged(
    #                 state="hovering", _timeout=10, _policy="check_wait")
    #         )
    #     )
    # ).wait()
    time.sleep(10)
    # assert drone(Landing()).wait().success()
    drone.disconnect()


if __name__ == "__main__":
    test_takeoff()
