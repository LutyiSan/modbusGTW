from loguru import logger
from config import create_config
from modbus_objects import Device

"""
1. Создаем конфигурации девайсов из csv файлов (create_devices)
"""


def create_devices():
    devices = create_config()
    if not devices:
        logger.error("Devices is not created! Check csv-files")
        return
    polling_devices = []
    for device in devices:
        polling_device = Device(device['device']['name'])
        polling_device.ip_address = device['device']['ip']
        polling_device.port = device['device']['port']
        polling_device.timeout = device['device']['timeout']
        polling_device.poll_period = device['device']['poll_period']
        polling_device.add_points(device['points'])
        polling_devices.append(polling_device)
        logger.debug(f"device {polling_device.name} created")
    logger.debug(f"All devices created")
    return polling_devices

create_devices()