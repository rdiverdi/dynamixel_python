import json
import pkg_resources
import time

import dynamixel_sdk as dxl


class InvalidDataSize(Exception):
    pass

class ReadError(Exception):
    pass

def get_control_table(name):
    table = pkg_resources.resource_stream(__name__, f'control_tables/{name}.json')
    return json.load(table)


class DynamixelMotor(object):
    def __init__(self, port_handler, packet_handler, json, dxl_id=1, name=''):
        self.id = dxl_id
        self.name = name
        
        self.portHandler = port_handler
        self.packetHandler = packet_handler

        self.setup_methods(json)
        
    def get_com_return(self, res, err):
        if res != dxl.COMM_SUCCESS:
            return False
        if err != 0:
            return False
        return True

    def ping(self):
        rsp, res, err = self.packetHandler.ping(self.portHandler, self.id)
        return self.get_com_return(res, err)

    def write_data(self, size, address, data):
        if size == 1:
            res, err = self.packetHandler.write1ByteTxRx(
                    self.portHandler, self.id, address, data)
        elif size == 2:
            res, err = self.packetHandler.write2ByteTxRx(
                    self.portHandler, self.id, address, data)
        elif size == 4:
            res, err = self.packetHandler.write4ByteTxRx(
                    self.portHandler, self.id, address, data)
        else:
            raise InvalidDataSize("write data called with size " + str(size))
        return self.get_com_return(res, err)

    def read_data(self, size, address):
        if size == 1:
            val, res, err = self.packetHandler.read1ByteTxRx(
                    self.portHandler, self.id, address)
        elif size == 2:
            val, res, err = self.packetHandler.read2ByteTxRx(
                    self.portHandler, self.id, address)
        elif size == 4:
            val, res, err = self.packetHandler.read4ByteTxRx(
                    self.portHandler, self.id, address)
        else:
            raise InvalidDataSize("write data called with size " + str(size))
        if not self.get_com_return(res, err):
            raise ReadError("packet handler responded with " + str(res))
        return val

    def setup_methods(self, json):
        full_list = json['eeprom']
        full_list.extend(json['ram'])
        for attrib_dict in full_list:
            name = next(iter(attrib_dict))
            attrib = next(iter(attrib_dict.values()))
            if 'r' in attrib["Access"].lower():
                setattr(
                        self,
                        'get_' + name.lower().replace(' ', '_'),
                        lambda size=int(attrib["Size(Byte)"]), addr=int(attrib["Address"]): \
                                self.read_data(size, addr)
                )
            if 'w' in attrib["Access"].lower():
                setattr(
                        self,
                        'set_' + name.lower().replace(' ', '_'),
                        lambda data, size=int(attrib["Size(Byte)"]), addr=int(attrib["Address"]): \
                                self.write_data(size, addr, data)
                )
    

class DynamixelManager(object):
    def __init__(self, usb_port='/dev/ttyUSB0', baud_rate=57600):
        self.dxl_dict = {}
        self.protocol = 2.0
        self.baud_rate = baud_rate
        self.portHandler = dxl.PortHandler(usb_port)
        self.packetHandler = dxl.PacketHandler(self.protocol)

    def __getitem__(self, key):
        return self.dxl_dict[key]

    def __iter__(self):
        return iter(self.dxl_dict.values())

    def init(self):
        if not self.portHandler.openPort():
            return False
        return self.portHandler.setBaudRate(self.baud_rate)

    def close(self):
        self.portHandler.closePort()
        return True

    def add_dynamixel_with_ctrl_table(self, dxl_name, dxl_id, ctrl_table):
        self.dxl_dict[dxl_name] = DynamixelMotor(
                self.portHandler, self.packetHandler, ctrl_table, dxl_id, dxl_name)
        return self.dxl_dict[dxl_name]

    def add_dynamixel(self, dxl_name, dxl_id, dxl_model):
        ctrl_table = get_control_table(dxl_model)
        return self.add_dynamixel_with_ctrl_table(dxl_name, dxl_id, ctrl_table)

    def ping_all(self):
        success = True
        for motor in self.dxl_dict.values():
            success &= motor.ping()
        return success

    def enable_all(self):
        success = True
        for motor in self.dxl_dict.values():
            success &= motor.set_torque_enable(True)
        return success

    def disable_all(self):
        success = True
        for motor in self.dxl_dict.values():
            success &= motor.set_torque_enable(False)
        return success

    def for_all(self, func):
        for motor in self.dxl_dict.values():
            func(motor)


