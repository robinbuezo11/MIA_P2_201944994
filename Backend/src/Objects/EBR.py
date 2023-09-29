import ctypes
import struct
from Utils.Utilities import coding_str

const = 'ssiii16s'
#ss son 2 strings de 1 byte, iii son 3 enteros de 4 bytes, 16s es un string de 16 bytes

class EBR(ctypes.Structure):

    _fields_ = [
        ('part_status', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('part_start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('part_next', ctypes.c_int),
        ('part_name', ctypes.c_char * 16)
    ]

    def __init__(self):
        self.part_status = b'\0'
        self.part_fit = b'\0'
        self.part_start = -1
        self.part_s = -1
        self.part_next = -1
        self.part_name = b'\0'*16

    def get_const(self):
        return const

    def _set_part_status(self, part_status):
        self.part_status = coding_str(part_status, 1)

    def _set_part_fit(self, part_fit):
        self.part_fit = coding_str(part_fit, 1)

    def _set_part_start(self, part_start):
        self.part_start = part_start

    def _set_part_s(self, part_s):
        self.part_s = part_s

    def _set_part_next(self, part_next):
        self.part_next = part_next

    def _set_part_name(self, part_name):
        self.part_name = coding_str(part_name, 16)
 
    def set_info(self, part_status, part_fit, part_start, part_s, part_next, part_name):
        self._set_part_status(part_status)
        self._set_part_fit(part_fit)
        self._set_part_start(part_start)
        self._set_part_s(part_s)
        self._set_part_next(part_next)
        self._set_part_name(part_name)
    
    def display_info(self):
        print("\n*** EBR ***")
        print("Estado: ", self.part_status.decode().upper())
        print("Ajuste: ", self.part_fit.decode().upper())
        print("Inicio: ", self.part_start)
        print(f"Tamaño: {self.part_s/1024} KB")
        print("Siguiente: ", self.part_next)
        print("Nombre: ", self.part_name.decode().upper(), "\n")

    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.part_status,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_next,
            self.part_name
        )
        return serialize
    
    def doDeserialize(self, data):
        self.part_status, self.part_fit, self.part_start, self.part_s, self.part_next, self.part_name = struct.unpack(const, data)

    def generate_report_mbr(self):
        return '''
        <tr>
            <td bgcolor="#5bff33"><b>Particion Logica</b></td>
        </tr>
        <tr>
            <td><b>part_status      </b> '''+self.part_status.decode().upper()+'''</td>
        </tr>
        <tr>
            <td><b>part_fit      </b> '''+self.part_fit.decode().upper()+'''</td>
        </tr>
        <tr>
            <td><b>part_start      </b> '''+str(self.part_start)+'''</td>
        </tr>
        <tr>
            <td><b>part_size      </b> '''+str(self.part_s)+'''</td>
        </tr>
        <tr>
            <td><b>part_next      </b> '''+str(self.part_next)+'''</td>
        </tr>
        <tr>
            <td><b>part_name      </b> '''+self.part_name.decode().upper()+'''</td>
        </tr>'''