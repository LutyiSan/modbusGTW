from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class Convertor:

    @staticmethod
    def converting(values, point):
        if point.quantity == 1:
            return Convertor.single_register(values, point)
        elif point.quantity == 2:
            return Convertor.two_registers(values, point)
        elif point.quantity == 4:
            return Convertor.four_registers(values, point)

    @staticmethod
    def single_register(values, point):
        if point.data_type == 'int':
            return Convertor.to_int16(values, point)
        elif point.data_type == 'uint':
            return Convertor.to_uint16(values, point)
        elif point.data_type == 'float':
            return Convertor.to_float16(values, point)
        elif point.data_type == 'bool':
            return Convertor.to_bool(values)
        elif point.data_type == 'bit':
            return Convertor.to_bit(values, point)

    @staticmethod
    def two_registers(values, point):
        if point.data_type == 'int':
            return Convertor.to_int32(values, point)
        elif point.data_type == 'uint':
            return Convertor.to_uint32(values, point)
        elif point.data_type == 'float':
            return Convertor.to_float32(values, point)

    @staticmethod
    def four_registers(values, point):
        if point.data_type == 'int':
            return Convertor.to_int64(values, point)
        elif point.data_type == 'uint':
            return Convertor.to_uint64(values, point)
        elif point.data_type == 'float':
            return Convertor.to_float64(values, point)

    @staticmethod
    def to_bool(value: int) -> bool or None:
        if not isinstance(value, int):
            return None
        else:
            if value:
                return True
            else:
                return False

    @staticmethod
    def to_bit(value: int, point) -> bool or None:
        if not isinstance(value, int):
            return None
        else:
            bv = Convertor.to_16bit_array(value)
            if bv is None:
                return None
            if int(bv[point.bit]) == 1:
                return True
            else:
                return False

    @staticmethod
    def to_16bit_array(value: int) -> str or None:
        if not isinstance(value, int):
            return None
        bin_value = bin(value)[2:]
        if len(bin_value) != 16:
            zero_array = ""
            count = 16 - len(bin_value)
            i = 0
            while i < count:
                i += 1
                zero_array += '0'
            zero_array += bin_value
            return zero_array
        else:
            return bin_value

    @staticmethod
    def to_uint16(value: int, point) -> int or None:
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(value, int):
            decoder = BinaryPayloadDecoder.fromRegisters([value], byteorder=bo, wordorder=Endian.Big)
            return decoder.decode_16bit_uint()
        else:
            return None

    @staticmethod
    def to_int16(value: int, point) -> int or None:
        if point.byte_order == 'little':
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(value, int):
            decoder = BinaryPayloadDecoder.fromRegisters([value], byteorder=bo, wordorder=Endian.Big)
            return decoder.decode_16bit_int()
        else:
            return None

    @staticmethod
    def to_int32(values: list[int], point) -> int or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                    return decoder.decode_32bit_int()
        else:
            return None

    @staticmethod
    def to_int64(values: list[int], point) -> int or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                    return decoder.decode_64bit_int()
        else:
            return None

    @staticmethod
    def to_uint32(values: list[int], point) -> int or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big

        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
            else:
                decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                return decoder.decode_32bit_uint()
        else:
            return None

    @staticmethod
    def to_uint64(values: list[int], point) -> int or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                    return decoder.decode_64bit_uint()
        else:
            return None

    @staticmethod
    def to_float16(values: int, point) -> float or None:
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, int):
            decoder = BinaryPayloadDecoder.fromRegisters([values], byteorder=bo, wordorder=Endian.Little)
            return decoder.decode_16bit_float()
        else:
            return None

    @staticmethod
    def to_float32(values: list[int], point) -> float or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                    return decoder.decode_32bit_float()
        else:
            return None

    @staticmethod
    def to_float64(values: list[int], point) -> float or None:
        if point.word_order == "little":
            wo = Endian.Little
        else:
            wo = Endian.Big
        if point.byte_order == "little":
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=bo, wordorder=wo)
                    return decoder.decode_64bit_float()
        else:
            return None
