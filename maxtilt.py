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

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
drone = olympe.Drone(DRONE_IP)


coordinates1 = (34,4253, 135.4269)
coordinates2 = (34.4255, 135.4268)
coordinates3 = (34.4253, 135.4265)
coordinates4 = (34.4252, 135.4265)

def main():
    listener = Listener(on_press=on_press) #anafi
    listener.start()

    drone.connect()

    takeOffDeff()

    # Get the home position 
    drone_location = drone.get_state(GpsLocationChanged)

    moveByFlont10(drone_location)

    moveToBackHome(drone_location)

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
    drone(
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
    ).wait()

def moveByFlont10(coordinates1):
    # Go back home
    drone(
        extended_move_to(34.4253,  135.4269,\
         1, MoveTo_Orientation_mode.TO_TARGET, 0.0, 1, 1, 1)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveToChanged(34,4253,\
         135.4269,\
         altitude=1, orientation_mode=MoveTo_Orientation_mode.TO_TARGET,\
         status='DONE', _policy='wait')
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()


def moveToBackHome(drone_location):
    # Go back home
    drone(
        extended_move_to(drone_location["latitude"],  drone_location["longitude"],\
         drone_location["altitude"], MoveTo_Orientation_mode.TO_TARGET, 0.0, 1, 1, 1)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"],\
         altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET,\
         status='DONE', _policy='wait')
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()


def landingDeff():
    # Landing
    drone(
        Landing()
        >> FlyingStateChanged(state="landed", _timeout=5)
    ).wait()

    
if __name__ == "__main__":
    main()