from os import path

from env import DEVICE_LIST
from schema import CSV


PREFIX = "devices"


def check_file(filepath: str, filenames: list):
    if not path.exists(filepath):
        return
    for f in filenames:
        if not path.isfile("/".join([filepath, f])):
            return
    return True


def check_headers(cols):
    params = []
    for k in CSV:
        params.append(k.value)
    for col in cols:
        if col not in params:
            return
    return cols


def csv_to_dict(csv_file: str, csv_delimiter: str):
    with open(f"{PREFIX}/{csv_file}", 'r') as fl:
        csv_txt = fl.read().splitlines()
    cols = check_headers(csv_txt[0].split(csv_delimiter))
    if not cols:
        return
    result_dict = dict.fromkeys(cols)
    for col in cols:
        result_dict[col] = []
    idx = 0
    rows = len(csv_txt) - 1
    while idx < rows:
        idx += 1
        row = csv_txt[idx].split(csv_delimiter)
        c = -1
        for col in cols:
            c += 1
            result_dict[col].append(row[c])
    return result_dict


def make_device(data):
    device = {'ip': data['ip'][0], 'port': data['port'][0], 'timeout': data['timeout'][0], "unit": data['unit'][0],
              'poll_period': data['poll_period'][0], 'name': data['topic'][0]}
    return device


def make_points(conf):
    points = []
    pi = 0
    while pi < len(conf['name']):
        point = {'name': conf['name'][pi],
                 'reg_type': conf['reg_type'][pi],
                 'reg_address': conf['reg_address'][pi],
                 'quantity': conf['quantity'][pi],
                 'bit_number': conf['bit_number'][pi],
                 'value_type': conf['value_type'][pi],
                 'scale': conf['scale'][pi],
                 'word_order': conf['word_order'][pi],
                 'byte_order': conf['byte_order'][pi]}
        points.append(point)
        pi += 1
    return points


def normalize_config_values(config: list):
    devices_conf = []
    for conf in config:
        device = {}
        for key in conf.keys():
            idx = 0
            while idx < len(conf[key]):
                if conf[key][idx].isdigit():
                    conf[key][idx] = int(conf[key][idx])
                elif conf[key][idx] == '':
                    conf[key][idx] = None
                idx += 1
        device['device'] = make_device(conf)
        device['points'] = make_points(conf)
        devices_conf.append(device)

    return devices_conf


def create_config():
    config_list = list()
    if check_file(PREFIX, DEVICE_LIST):
        for d in DEVICE_LIST:
            config = csv_to_dict(d, ";")
          #  print(config)
            if config:
                config_list.append(config)
            else:
                return
    normal_data = normalize_config_values(config_list)
    #print(normal_data)
    if normal_data:
        return normal_data




