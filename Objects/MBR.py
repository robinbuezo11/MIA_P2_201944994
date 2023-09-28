import ctypes
import struct
import random
from Utils.Utilities import coding_str

const = 'I19sI' 
#I es un entero de 4 bytes, 19s es un string de 26 bytes, I es un entero de 4 bytes

class MBR(ctypes.Structure):

    _fields_ = [
        ('mbr_tamano', ctypes.c_int),
        ('mbr_fecha_creacion', ctypes.c_char * 19),
        ('mbr_dsk_signature', ctypes.c_int)
    ]

    def __init__(self):
        self.mbr_tamano = 0
        self.mbr_fecha_creacion = b'\0'*19
        self.mbr_dsk_signature = 0

    def _set_mbr_tamano(self, mbr_tamano):
        self.mbr_tamano = mbr_tamano

    def _set_mbr_fecha_creacion(self, mbr_fecha_creacion):
        self.mbr_fecha_creacion = coding_str(mbr_fecha_creacion, 19)

    def _set_mbr_dsk_signature(self, mbr_dsk_signature):
        self.mbr_dsk_signature = mbr_dsk_signature
 
    def set_info(self, mbr_fecha_creacion, mbr_tamano):
        self._set_mbr_tamano(mbr_tamano)
        self._set_mbr_fecha_creacion(mbr_fecha_creacion)
        self._set_mbr_dsk_signature(random.randint(1, 1000000))
    
    def display_info(self):
        print("Tamaño: ", self.mbr_tamano)
        print("Fecha de creacion: ", self.mbr_fecha_creacion.decode())
        print("Signature: ", self.mbr_dsk_signature)

    def doSerialize(self):
        return struct.pack(
            const,
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature
        )
    
    def doDeserialize(self, data):
        self.mbr_tamano, self.mbr_fecha_creacion, self.mbr_dsk_signature = struct.unpack(const, data)

