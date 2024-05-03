# -*- coding: utf-8 -*-
import logging
import math
import traceback
from datetime import datetime

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from base.plugin import Plugin
from base.messages import log_messages
from base.settings import decode_map_coils, decode_map_registers, max_bulk_read_holding_registers
from logger.defaults import settings as log_settings

logging.getLogger('pymodbus').setLevel(logging.ERROR)


class Reader(Plugin):
    """
    Reader plugin get registers values from PLC.
    """

    def __init__(self, variable_map_file, client_directory, plc_host, plc_port, device_id):
        """ Constructor for Reader. """
        self.messages = log_messages(self.__class__.__name__)
        log_file = log_settings.get('reader_log_file').format(device_id=device_id)
        super().__init__(variable_map_file, log_file, client_directory, self.messages)

        self.plc_host = plc_host
        self.plc_port = plc_port
        self.device_id = device_id
        self.logger.debug(plc_host)
        self.variable_map = self.read_file(self.device_id)
        self.coils_address = self._coil_address()
        self.holding_registers_address = self._holding_registers_address()
        self.client, connected = self._connect(self.plc_host, self.plc_port)
        if self.client is None or not connected:
            raise ConnectionError("Modbus connection failed")

    def __del__(self):
        """
        Destruct of Reader.
        """
        if hasattr(self, 'client'):
            self._close(self.client)

    def _get_address_from_dict(self, kind, key):
        """
        Method to get address from dictionary

        :param kind: Name of kind
        :type kind: str
        :param key: Address value
        :type key: str
        :return: List of addresses
        :rtype: list
        """
        return [address.get(key) for address in self.variable_map.get(kind)]

    def _coil_address(self):
        """
        Method to get coil address

        :return: List of coil addresses
        :rtype: list
        """
        return self._get_address_from_dict('coils', 'Address_1')

    def _holding_registers_address(self):
        """
        Method to get holding registers address

        :return: List of register addresses
        :rtype: list
        """
        return self._get_address_from_dict('holding_registers', 'Address_1')

    def _max_coils_address(self):
        """
        Method to define max value from coils addresses

        :return: Maximum value of coil addresses
        :rtype: int
        """
        return max(self.coils_address)

    def _min_coils_address(self):
        """
        Method to define min value from coils addresses

        :return: Minimum value of coil addresses
        :rtype: int
        """
        return min(self.coils_address)

    def _max_holding_registers(self):
        """
        Method to define max value from holding registers addresses

        :return: Maximum value of register addresses
        :rtype: int
        """
        return max(self.holding_registers_address)

    def _min_holding_registers(self):
        """
        Method to define min value from holding registers addresses

        :return: Minimum value of register addresses
        :rtype: int
        """
        return min(self.holding_registers_address)

    @staticmethod
    def _is_simple_data(data_type):
        """
        Check if data type is bit or int16

        :param data_type: Data type
        :type data_type: str
        :return: Status on data type
        :rtype: bool
        """
        return data_type in ['BIT', 'INT16']

    def _increase_address(self, data_type):
        """
        Method for setting positions according to date type

        :param data_type: Name of data type
        :type data_type: str
        :return: Increment to address
        :rtype: int
        """
        increase = 0
        if not self._is_simple_data(data_type):
            increase += 2
        return increase

    def _read_coils_addresses(self):
        """
        Method to read coils addresses

        :return: List of coil addresses
        :rtype: list
        """
        coils_addresses = []
        try:
            data = self.client.read_coils(self._min_coils_address(), self._max_coils_address())
        except Exception as error:
            self.logger.debug(self.messages.get('msg_unknown_error', 'msg_unknown_error').format(error=error))
        else:
            if not hasattr(data, 'bits'):
                self.logger.debug(str(data))
            else:
                coils_addresses = data.bits
        return coils_addresses

    def _read_holding_registers_addresses(self, payload):
        """
        Method to read holding registers addresses

        :param payload: Data
        :type payload: list
        :return: List of holding registers
        :rtype: list
        """
        response = []
        try:
            min_holding_registers = self._min_holding_registers()
            max_holding_registers = self._max_holding_registers() + self._increase_address(payload[-1].get('DataType'))
            addresses_range = range(min_holding_registers, max_holding_registers, max_bulk_read_holding_registers)
            for index, start in enumerate(addresses_range):
                end = max_bulk_read_holding_registers
                if index == len(addresses_range) - 1:
                    end = max_holding_registers - start
                result = self.client.read_holding_registers(start, end)
                if not hasattr(result, 'registers'):
                    self.logger.debug(str(result))
                else:
                    response += result.registers
        except Exception as error:
            trace_msg = ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '||')
            self.logger.debug(
                self.messages.get('msg_read_holding_error', 'msg_read_holding_error').format(
                    error=error,
                    trace_msg=trace_msg
                )
            )
        return response

    def read_coils(self):
        """
        Method to return payload of coils registers

        :return: List of coil registers
        :rtype: list
        """
        payload = self.variable_map.get('coils').copy()
        try:
            read_coils_addresses = self._read_coils_addresses()
            for coil in payload:
                response = [read_coils_addresses[coil.get('Address_1')]]
                decoder = BinaryPayloadDecoder.fromCoils(response, byteorder=Endian.Big, wordorder=Endian.Big)
                response = getattr(decoder, decode_map_coils.get(coil.get('DataType')))()
                coil['response'] = response
                coil['kind'] = 'coil'
                coil['timestamp'] = str(datetime.now())
        except Exception as error:
            trace_msg = ''.join(traceback.format_tb(error.__traceback__)).replace('\n', '||')
            self.logger.debug(
                self.messages.get('msg_read_coils_error', 'msg_read_coils_error').format(
                    error=error,
                    trace_msg=trace_msg
                )
            )
        return payload

    def _decode_32bit(self, payload):
        """
        Method to decode a 32bit value
        
        :param payload: Data
        :type payload: list
        :return: decoded int32 value
        :rtype: int
        """
        int32_value = payload[1] * 65536 + payload[0]
        return int32_value

    def read_holding_registers(self):
        """
        Method to return payload of holding registers

        :return: List of holding registers
        :rtype: list
        """
        payload = self.variable_map.get('holding_registers').copy()
        try:
            read_holding_registers = self._read_holding_registers_addresses(payload)
            for register in payload:
                response = [read_holding_registers[register.get('Address_1')]]
                if not self._is_simple_data(register.get('DataType')):
                    if register.get('DataType') == 'STRING':
                        response = read_holding_registers[register.get('Address_1'): register.get('Address_1') + 32]
                    else:
                        response = read_holding_registers[register.get('Address_1'): register.get('Address_1') + 2]
                decoder = BinaryPayloadDecoder.fromRegisters(response, byteorder=Endian.Big, wordorder=Endian.Big)
                if register.get('DataType') == 'STRING':
                    response = getattr(decoder, 'decode_string')(32).decode().strip('\u0000')
                elif register.get('DataType') == 'INT32':
                    response = self._decode_32bit(response)
                else:
                    response = getattr(decoder, decode_map_registers.get(register.get('DataType')))()
                register['response'] = response
                register['kind'] = 'holding_register'
                register['timestamp'] = str(datetime.now())
        except Exception as error:
            self.logger.debug(self.messages.get('msg_unknown_error', 'msg_unknown_error').format(error=error))
        return payload

   

    @staticmethod
    def to_dict(list_objects):
        """Method to transform data in json format

        :param list_objects: List of objects
        :type list_objects: list
        :return: Json formatted string
        :rtype: str
        """
        data = {}
        for obj in list_objects:
            if isinstance(obj.get('response'), float):
                if math.isnan(obj.get('response')):
                    data[obj.get('Name')] = None
                else:
                    data[obj.get('Name')] = obj.get('response')
            else:
                data[obj.get('Name')] = obj.get('response')
        return data

    def run(self):
        """ Method to execute all process of Reader. """
        self.logger.debug(self.messages.get('msg_starting', 'msg_starting').format(plugin_name='reader'))
        coils = self.read_coils()
        holding_registers = self.read_holding_registers()
        list_data = coils + holding_registers
        data = self.to_dict(list_data)
        self.logger.debug(self.messages.get('msg_finishing', 'msg_finishing').format(plugin_name='reader'))
        return data
