import math
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD, Emergency
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from pynput.keyboard import Listener, KeyCode

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
drone = olympe.Drone(DRONE_IP)


def main():
    listener = Listener(on_press=on_press)
    listener.start()

    drone.connect()

    takeOffDeff()

    # Get the home position 
    drone_location = drone.get_state(GpsLocationChanged)

    moveByFlont10()

    moveToBackHome(drone_location)

    landingDeff()

    drone.disconnect()


def on_press(key):
    if key == KeyCode.from_char('e'):
        print('EMERGENCY cutoff triggered')
        drone(Emergency())

    if key == KeyCode.from_char('l'):
        print('Landing')
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


def moveByFlont10():
    # Move 10m
    drone(
        moveBy(50, 0, 0, math.pi)
        #>> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()


def moveToBackHome(drone_location):
    # Go back home
    drone(
        moveTo(drone_location["latitude"],  drone_location["longitude"], drone_location["altitude"], MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
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