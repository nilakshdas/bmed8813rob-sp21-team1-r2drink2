import inputs

from inputs import DeviceManager
from inputs import get_gamepad

devices = DeviceManager()

while 1:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)

