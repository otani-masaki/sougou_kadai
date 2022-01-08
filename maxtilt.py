import olympe
import os
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.ardrone3.PilotingSettingsState import MaxTiltChanged
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD, Emergency

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")


def test_maxtilt():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    # maxTiltAction = drone(MaxTilt(10)).wait()
    # if maxTiltAction.success():
    #     print("MaxTilt(10) success")
    # elif maxTiltAction.timedout():
    #     print("MaxTilt(10) timedout")
    # else:
    #     # If ".wait()" is called on the ``maxTiltAction`` this shouldn't happen
    #     print("MaxTilt(10) is still in progress")
    # maxTiltAction = drone(MaxTilt(0)).wait()
    # if maxTiltAction.success():
    #     print("MaxTilt(0) success")
    # elif maxTiltAction.timedout():
    #     print("MaxTilt(0) timedout")
    # else:
    #     # If ".wait()" is called on the ``maxTiltAction`` this shouldn't happen
    #     print("MaxTilt(0) is still in progress")
    drone(TakeOff()).wait().success()

    drone(MaxTilt(1)
        >> MaxTiltChanged(1,1,1)
    ).wait().success()
    
    drone(moveBy(10,0,0,0)).wait().success()

    drone.disconnect()


if __name__ == "__main__":
    test_maxtilt()





