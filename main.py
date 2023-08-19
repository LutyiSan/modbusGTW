from time import sleep
from loguru import logger
from config import create_config
from modbus_objects import Device
from modbus_pymodbus import TCPClient
from convertor import Convertor
from mqtt import MyMQTT
from env import *


def prepare_data_for_mqtt(device):
    points = {}
    for p in device.points:
        points[p.name] = p.present_value
    return points


class GTW:
    def __init__(self, source='file', recip='mqtt'):
        self.devices = None
        self.source = source
        self.recipient = recip
        self.mqtt_client = MyMQTT()

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

    def __read_points(self):
        client = TCPClient()
        for d in self.poll_devices:
            if not client.connection(d.ip_address, d.port):
                return
            if not MULTI_READ:
                for point in d.points:
                    result = client.read_single(point, unit=d.unit)
                    if result:
                        point.present_value = Convertor.converting(result, point)
                    else:
                        point.present_value = 'fault'
                        d.is_fault = True
            client.disconnect()

    def run_time(self):
        self.mqtt_client.create(USER_NAME, USE_PASSWD)
        self.__read_points()
        if RECIPIENT == 'mqtt':
            if self.mqtt_client.connect(BROKER, BROKER_PORT):
                for d in self.poll_devices:
                    self.mqtt_client.send(TOPIC, prepare_data_for_mqtt(d))
                self.mqtt_client.disconnect()



gtw = GTW()
gtw.create_devices()

gtw.run_time()
