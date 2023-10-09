import ctypes
import struct
from Utils.Utilities import coding_str

const = 'i 12s'

class Content(ctypes.Structure):
    _fields_ = [
        ("b_inodo", ctypes.c_int),
        ("b_name", ctypes.c_char * 12)
    ]

    def __init__(self):
        self.b_inodo = -1
        self.b_name = b'\0'*12 
 
    def getConst(self):
        return const
    
    def setInodo(self, inodo):
        self.b_inodo = inodo

    def setName(self, name):
        self.b_name = coding_str(name, 12)

    def setInfo(self, inodo, name):
        self.setInodo(inodo)
        self.setName(name)

    def display_info(self):
        print("b_inodo: ", self.b_inodo)
        print("b_name: ", self.b_name, "\n")

    def doSerialize(self):
        serialize =  struct.pack(
            const,
            self.b_inodo,
            self.b_name
        )
        return serialize
    
    def doDeserialize(self, data):
        self.b_inodo,self.b_name = struct.unpack(const, data)

    def generate_report_block(self):
        code = '''
        <tr>
            <td><b>b_inodo      </b> '''+str(self.b_inodo)+'''</td>
        </tr>
        <tr>
            <td><b>b_name      </b> '''+self.b_name.decode()+'''</td>
        </tr>'''
        return code
    
    def generate_report_tree(self):
        code = f'''
        <tr>
            <td>{self.b_name.decode()}</td><td>{self.b_inodo}</td>
        </tr>'''
        return code