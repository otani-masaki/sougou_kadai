import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, Emergency
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from pynput.keyboard import Listener, KeyCode


def on_press(key):
    if key == KeyCode.from_char('e'):
        print('EMERGENCY cutoff triggered')
        drone(Emergency())


listener = Listener(on_press=on_press)
listener.start()


with olympe.Drone("10.202.0.1") as drone:
    drone.connect()

    # Start a flying action asynchronously
    flyingAction = drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveBy(10, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> Landing()
    )

    # press 'e' here will send the Emergency message

    # Wait for the end of the flying action
    if not flyingAction.wait().success():
        raise RuntimeError("Cannot complete the flying action")

    # Leaving the with statement scope: implicit drone.disconnection()
    # drone.disconnect()