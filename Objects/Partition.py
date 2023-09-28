import ctypes
import struct
from Utils.Utilities import coding_str

const = 'sssii16s' 

class Partition(ctypes.Structure):

    _fields_ = [
        ('part_status', ctypes.c_char),
        ('part_type', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('part_start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('part_name', ctypes.c_char * 16)
    ]

    def __init__(self):
        self.part_status = b'\0'
        self.part_type = b'\0'
        self.part_fit = b'\0'
        self.part_start = 0
        self.part_s = 0
        self.part_name = b'\0'*16

    def _set_part_status(self, part_status):
        self.part_status = coding_str(part_status, 1)

    def _set_part_type(self, part_type):
        self.part_type = coding_str(part_type, 1)

    def _set_part_fit(self, part_fit):
        self.part_fit = coding_str(part_fit, 1)

    def _set_part_start(self, part_start):
        self.part_start = part_start

    def _set_part_s(self, part_s):
        self.part_s = part_s

    def _set_part_name(self, part_name):
        self.part_name = coding_str(part_name, 16)
 
    def set_info(self, part_status, part_type, part_fit, part_start, part_s, part_name):
        self._set_part_status(part_status)
        self._set_part_type(part_type)
        self._set_part_fit(part_fit)
        self._set_part_start(part_start)
        self._set_part_s(part_s)
        self._set_part_name(part_name)
    
    def display_info(self):
        print("Status: ", self.part_status.decode())
        print("Type: ", self.part_type.decode())
        print("Fit: ", self.part_fit.decode())
        print("Start: ", self.part_start)
        print("Size: ", self.part_s)
        print("Name: ", self.part_name.decode())

    def doSerialize(self):
        return struct.pack(
            const,
            self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_name
        )
    
    def doDeserialize(self, data):
        self.part_status, self.part_type, self.part_fit, self.part_start, self.part_s, self.part_name = struct.unpack(const, data)

