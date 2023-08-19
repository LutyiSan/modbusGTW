from loguru import logger
from config import create_config
from modbus_objects import Device
from modbus_pymodbus import TCPClient
from convertor import Convertor


class GTW:
    def __init__(self, source='file', recip='mqtt'):
        self.devices = None
        self.source = source
        self.recipient = recip

    def create_devices(self):
        match self.source:
            case 'file':
                self.__from_files()

    def __from_files(self):
        self.devices = create_config()
        if not self.devices:
            logger.error("Devices is not created! Check csv-files")
            return
        self.poll_devices = []
        for device in self.devices:
            polling_device = Device(device['device']['name'])
            polling_device.ip_address = device['device']['ip']
            polling_device.port = device['device']['port']
            polling_device.timeout = device['device']['timeout']
            polling_device.unit = device['device']['unit']
            polling_device.poll_period = device['device']['poll_period']
            polling_device.add_points(device['points'])
            self.poll_devices.append(polling_device)
            logger.debug(f"Device {polling_device.name} created")
            logger.debug(f"All devices created")

    def read_points(self):
        client = TCPClient()
        for d in self.poll_devices:
            if not client.connection(d.ip_address, d.port):
                return
            for point in d.points:
                result = client.read_single(point, unit=d.unit)
                if result:
                    point.present_value = Convertor.converting(result, point)
                else:
                    point.present_value = 'fault'
                    d.is_fault = True


gtw = GTW()
gtw.create_devices()
gtw.read_points()
