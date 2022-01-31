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
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, Emergency, PCMD
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

    moveByFlont10(34.425520, 135.427167-0.0002)
    # moveByFlont10(34.425520-0.0001, 135.427167-0.0002)
    # moveByFlont10(34.425520-0.0001, 135.427167)
    moveByFlont10(34.425520, 135.427167)
    moveByFlont10(34.425520-0.0001, 135.427167-0.0002)

    # moveByFlont10(drone_location["latitude"], drone_location["longitude"]-0.0002)
    # moveByFlont10(drone_location["latitude"]-0.0001, drone_location["longitude"]-0.0002)
    # moveByFlont10(drone_location["latitude"]-0.0001, drone_location["longitude"])
    # moveByFlont10(drone_location["latitude"], drone_location["longitude"])


    # moveToBackHome(drone_location)

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

def moveByFlont10(latitude, longitude):
    # Go back home
    drone(
        extended_move_to(latitude,  longitude,\
         2, MoveTo_Orientation_mode.TO_TARGET, 0.0, 5, 1, 1)
        # >> FlyingStateChanged(state="hovering", _timeout=5)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> moveToChanged(latitude=latitude, longitude=longitude,\
         altitude=2, orientation_mode=MoveTo_Orientation_mode.TO_TARGET,\
         status='DONE', _policy='wait') 
        # >> FlyingStateChanged(state="hovering", _timeout=10)
    ).wait()


def moveToBackHome(drone_location):
    # Go back home
    assert drone(
        extended_move_to(latitude = drone_location["latitude"],  longitude = drone_location["longitude"],\
         altitude = 2, orientation_mode = MoveTo_Orientation_mode.TO_TARGET, heading = 0.0,\
         max_horizontal_speed = 1, max_vertical_speed = 1, max_yaw_rotation_speed = 1)
        >> moveToChanged(status='DONE')
        >> FlyingStateChanged(state="hovering", _timeout=10)
    ).wait()


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
    ).wait().success()

    
if __name__ == "__main__":
    main()