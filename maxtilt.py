"""
takeoff 
-> 10meters forward 
-> return to takeoff point 
-> landing
"""
import math
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD, Emergency
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from pynput.keyboard import Listener, KeyCode
from olympe.messages.move import extended_move_by, extended_move_to
from olympe.messages.ardrone3.PilotingEvent import moveByEnd


DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
drone = olympe.Drone(DRONE_IP)


def main():
    listener = Listener(on_press=on_press)
    listener.start()

    drone.connect()

    takeOffDeff()

    # Get the home position 
    drone_location = drone.get_state(GpsLocationChanged)
    print("==========================================================")
    print(drone_location)
    print("============================================================")
    culc1=drone_location["latitude"]*10000000000
    culc1=math.floor(culc1)
    print(culc1)
    culc1=culc1/10000000000
    print(culc1)

    culc2=drone_location["longitude"]*10000000000
    culc2=math.floor(culc2)
    print(culc2)
    culc2=culc2/10000000000
    print(culc2)

    moveByFlont10(10)

    drone_location = drone.get_state(GpsLocationChanged)
    print("==========================================================")
    print(drone_location)
    print("============================================================")

    moveToBackHome(drone_location, culc1, culc2)

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


def moveByFlont10(dx):
    # Move 10m
    drone(
        extended_move_by(dx, 0, 0, math.pi, 0.1, 0.1, 1, _timeout=100)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()


def moveToBackHome(drone_location, culc1, culc2):
    # Go back home
    drone(
        extended_move_to(culc1,  culc2,\
         1, MoveTo_Orientation_mode.TO_TARGET, 0.0, 10, 10, 10)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveToChanged(latitude=culc1, longitude=culc2,\
         altitude=1, orientation_mode=MoveTo_Orientation_mode.TO_TARGET,\
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