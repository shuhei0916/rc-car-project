# from evdev import InputDevice, list_devices
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
    print(f"Device: {device.name}, Path: {device.path}")
    
device_path = '/dev/input/event7'

gamepad = evdev.InputDevice(device_path)

print(f"Monitoring input from: {gamepad.name}")

# Read input
try:
    for event in gamepad.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print(evdev.categorize(event))
        elif event.type ==  evdev.ecodes.EV_ABS:
            print(f"Analog input: {event.code} Value: {event.value}")
except KeyboardInterrupt:
    print("Monitoring stopped.")
