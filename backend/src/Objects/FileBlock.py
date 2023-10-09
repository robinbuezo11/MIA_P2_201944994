import ctypes
import struct
from Utils.Utilities import coding_str

const = '64s'

class FileBlock(ctypes.Structure):

    _fields_ = [
        ('b_content', ctypes.c_char * 64)
    ]

    def __init__(self):
        self.b_content = b'\0'*64

    def get_const(self):
        return const
    
    def setInfo(self, content):
        self.b_content = coding_str(content, 64)

    def display_info(self):
        print("\nBloque de Archivo")
        print("b_content: ", self.b_content.decode(), "\n")
    
    def doSerialize(self): 
        return struct.pack(
            const,
            self.b_content
        )

    def doDeserialize(self, data):
        self.b_content = struct.unpack(const, data)[0]
            

    def generate_report_block(self, index):
        code = '''
        <tr>
            <td bgcolor="#3371ff"><b>Bloque Archivo '''+str(index)+'''</b></td>
        </tr>
        <tr>
            <td><b>b_content      </b> '''+self.b_content.decode()+'''</td>
        </tr>'''
        return code
    
    def generate_report_tree(self, index):
        code = f'''
        file{index} [label=<<table cellspacing="0" cellpadding="2">
            <tr>
                <td bgcolor="#3371ff"><b>Bloque Archivo{index}</b></td>
            </tr>
            <tr>
                <td>{self.b_content.decode()}</td>
            </tr>
        </table>>];
        '''
        return code