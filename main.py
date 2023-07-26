
from config import create_config

devices = create_config()
if devices:
    print(devices[0])