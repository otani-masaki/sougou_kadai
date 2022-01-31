"""
takeoff 
-> move by specify the coordinates on "move to()" 
-> return to takeoff point 
-> landing 
"""
import math
from moveto import takeOffDeff
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, Emergency
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from olympe.messages.move import extended_move_by, extended_move_to
from pynput.keyboard import Listener, KeyCode

# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
drone = olympe.Drone(DRONE_IP)


def main():
    listener = Listener(on_press=on_press) #anafi
    listener.start()

    drone.connect()

    takeOffDeff()

    # Get the home position 
    drone_location = drone.get_state(GpsLocationChanged)

    landingDeff()

    drone.disconnect()

def on_press(key):
    if key == KeyCode.from_char('e'):
        print('EMERGENCY cutoff triggered')
        drone(Emergency())

    if key == KeyCode.from_char('l'):
        print('Landing triggered')
        drone(Landing())

    drone.disconnect()
        
def takeOffDeff():
    # Take-off
    assert drone(
        FlyingStateChanged(state="hovering", _policy="check")
        | FlyingStateChanged(state="flying", _policy="check")
        | (
            GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
            >> (
                TakeOff(_no_expect=True)
                & FlyingStateChanged(
                    state="hovering", _timeout=10, _policy="check_wait")
            )
        )
    ).wait(5)


def landingDeff():
    # Landing
    assert drone(
        FlyingStateChanged(state="landing", _policy="check")
        | FlyingStateChanged(state="flying", _policy="check")
        | (
            GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
            >> (
                Landing(_no_expect=True)
                & FlyingStateChanged(
                    state="landed", _timeout=5, _policy="check_wait")
            )
        )        
    ).wait()

    
if __name__ == "__main__":
    main()