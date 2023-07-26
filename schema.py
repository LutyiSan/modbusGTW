from enum import Enum, unique


@unique
class CSV(Enum):
    ip = 'ip'
    port = 'port'
    timeout = 'timeout'
    poll_period = 'poll_period'
    reg_type = 'reg_type'
    reg_address = 'reg_address'
    quantity = 'quantity'
    bit_number = 'bit_number'
    value_type = 'value_type'
    word_order = 'word_order'
    byte_order = 'byte_order'
    scale = 'scale'
    name = 'name'
    topic = 'topic'


@unique
class RegTypes(Enum):
    coils = 1
    discrete_inputs = 2
    holding_registers = 3
    input_registers = 4


@unique
class DataTypes(Enum):
    boolean = "bool"
    uint16 = 'uint16'
    uint32 = 'uint32'
    uint64 = 'uint64'
    int16 = 'int16'
    int32 = 'int32'
    int64 = 'int64'
    float16 = 'float16'
    float32 = 'float32'
    float64 = 'float64'
    bit = 'bit'


class RegAddress:
    min = 0
    max = 65535


class Quantity:
    min = 1
    max = 4


class Bit:
    min = 0
    max = 16
    default = None


class Order:
    big = 'big'
    little = 'little'
    default = 'big'


class Port:
    min = 1
    max = 65535
    default = 502


class PollPeriod:
    min = 0
    max = 86400
    default = 30


class Timeout:
    min = 1
    max = 30
    default = 3
