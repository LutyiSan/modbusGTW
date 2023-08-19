from pymodbus.client import ModbusTcpClient as ModbusClient
from loguru import logger


class TCPClient:
    def __init__(self):
        self.client = None

    def connection(self, ip_address, tcp_port=502, timeout=3):
        try:
            self.client = ModbusClient(ip_address, port=tcp_port, timeout=timeout)
            if self.client.connect():
                logger.debug(f"READY connection {ip_address}")
                return True
            else:
                logger.error(f"FAIL connection {ip_address}")
                return
        except Exception as e:
            logger.exception(f"FAIL connect {ip_address}", e)
            return

    def read_single(self, point, unit=1):
        match point.reg_type:
            case 1:
                return self.__read_coils(point.reg_address, point.quantity, unit)
            case 2:
                return self.__read_di(point.reg_address, point.quantity, unit)
            case 3:
                return self.__read_hr(point.reg_address, point.quantity, unit)
            case 4:
                return self.__read_ir(point.reg_address, point.quantity, unit)

    def __read_hr(self, reg_number, quantity, unit):
        try:
            result = self.client.read_holding_registers(reg_number, quantity, unit=hex(unit))
            return result.registers
        except Exception as e:
            logger.error("Can't Read registers\n", e)
            return

    def __read_ir(self, reg_number, quantity, unit):
        try:
            result = self.client.read_input_registers(reg_number, quantity, unit=hex(unit))
            return result.registers
        except Exception as e:
            logger.error("Can't Read registers\n", e)
            return False

    def __read_coils(self, reg_number, quantity, unit):
        out = []
        try:
            result = self.client.read_coils(reg_number, quantity, unit=hex(unit))
            for i in range(0, quantity):
                out.append(result.bits[i])
            return out
        except Exception as e:
            logger.error("Can't Read registers\n", e)
            return

    def __read_di(self, reg_number, quantity, unit):
        out = []
        try:
            result = self.client.read_discrete_inputs(reg_number, quantity, unit=hex(unit))
            for i in range(0, quantity):
                out.append(result.bits[i])
            return
        except Exception as e:
            logger.error("Can't Read registers\n", e)
            return False

    def disconnect(self):
        try:
            self.client.close()
            logger.debug("Connection closed")
        except Exception as e:
            logger.error("Can't close connection", e)


