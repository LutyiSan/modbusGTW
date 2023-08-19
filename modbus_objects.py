from schema import *


class Point:
    def __init__(self, name):
        self.name = name
        self.reg_type = None
        self.reg_address = None
        self.quantity = None
        self.bit_number = None
        self.data_type = None
        self.scale = None
        self.word_order = None
        self.byte_order = None
        self.present_value = None

    @property
    def reg_type(self):
        return self.__reg_type

    @reg_type.setter
    def reg_type(self, value):
        data_enum = [item.value for item in RegTypes]
        self.__reg_type = validate_in_enum(data_enum, value)

    @property
    def reg_address(self):
        return self.__reg_address

    @reg_address.setter
    def reg_address(self, value):
        self.__reg_address = validate_digit(value, RegAddress.min, RegAddress.max)

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = validate_digit(value, Quantity.min, Quantity.max)

    @property
    def bit_number(self):
        return self.__bit_number

    @bit_number.setter
    def bit_number(self, value):
        if value is None:
            self.__bit_number = Bit.default
        else:
            self.__bit_number = validate_digit(value, Bit.min, Bit.max)

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, value):
        data_enum = [item.value for item in DataTypes]
        self.__data_type = validate_in_enum(data_enum, value)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        if isinstance(value, (int, float)):
            self.__scale = value
        else:
            self.__scale = 1

    @property
    def word_order(self):
        return self.__word_order

    @word_order.setter
    def word_order(self, value):
        self.__word_order = validate_in_enum([Order.big, Order.little], value)
        if self.__word_order is None:
            self.__word_order = Order.default

    @property
    def byte_order(self):
        return self.__byte_order

    @byte_order.setter
    def byte_order(self, value):
        self.__byte_order = validate_in_enum([Order.big, Order.little], value)
        if self.__byte_order is None:
            self.__byte_order = Order.default

    def __repr__(self):
        return f"name: {self.name}\n  reg_type: {self.reg_type}\n  reg_address: {self.reg_address}\n" \
               f"  quantity: {self.quantity}\n  bit_number: {self.bit_number}\n  data_type: {self.data_type}\n  " \
               f"scale: {self.scale}\n  word_order: {self.word_order}\n  byte_order: {self.byte_order}"


class Device:

    def __init__(self, name):
        self.ip_address = None
        self.port = None
        self.poll_period = None
        self.timeout = None
        self.unit = None
        self.name = name
        self.is_fault = None
        self.status = None
        self.points = []

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value):
        self.__unit = validate_digit(value, Unit.min, Unit.max)
        if self.__unit is None:
            self.__unit = Unit.default

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value):
        self.__ip_address = validate_ip(value)

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = validate_digit(value, Port.min, Port.max)
        if self.__port is None:
            self.__port = Port.default

    @property
    def poll_period(self):
        return self.__poll_period

    @poll_period.setter
    def poll_period(self, value):
        self.__poll_period = validate_digit(value, PollPeriod.min, PollPeriod.max)
        if self.__poll_period is None:
            self.__poll_period = PollPeriod.default

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.__timeout = validate_digit(value, Timeout.min, Timeout.max)
        if self.__timeout is None:
            self.__timeout = Timeout.default

    def add_points(self, points):
        for point in points:
            p = Point(point['name'])
            p.reg_type = point['reg_type']
            p.reg_address = point['reg_address']
            p.quantity = point['quantity']
            p.bit_number = point['bit_number']
            p.data_type = point['value_type']
            p.word_order = point['word_order']
            p.byte_order = point['byte_order']
            p.scale = point['scale']
            self.points.append(p)

    def __repr__(self):
        return f"name: {self.name}\n  tp-address: {self.ip_address}\n  port: {self.port}\n"


def validate_ip(test_data):
    if not isinstance(test_data, str):
        return
    a = test_data.split('.')
    if len(a) != 4:
        return
    for x in a:
        if not x.isdigit():
            return
        i = int(x)
        if i < 0 or i > 255:
            return
    return test_data


def validate_digit(test_data, start, stop):
    if isinstance(test_data, (int, float)):
        if start <= test_data <= stop:
            return test_data


def validate_in_enum(enum, test_data):
    if test_data in enum:
        return test_data
