from config import create_config
from modbus_objects import Device


devices = create_config()
if devices:
    polling_devices = []
    for device in devices:
        polling_device = Device(device['device']['name'])
        polling_device.ip_address = device['device']['ip']
        polling_device.port = device['device']['port']
        polling_device.timeout = device['device']['timeout']
        polling_device.poll_period = device['device']['poll_period']
        polling_device.add_points(device['points'])
        polling_devices.append(polling_device)
        print(polling_device)
        print(polling_device.points[0])
