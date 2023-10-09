import ctypes
import struct

const = '16i'

class PointersBlock(ctypes.Structure):
    
        _fields_ = [
            ('b_pointers', ctypes.c_int * 16)
        ]
    
        def __init__(self):
            self.b_pointers = (ctypes.c_int * 16)(*[-1]*16)
    
        def getConst(self):
            return const
        
        def setInfo(self, pointers):
            self.b_pointers = pointers
    
        def display_info(self):
            print("\nBloque de Punteros")
            print("b_pointers: ", self.b_pointers, "\n")
        
        def doSerialize(self): 
            return struct.pack(
                const,
                *self.b_pointers
            )
    
        def doDeserialize(self, data):
            *self.b_pointers, = struct.unpack(const, data) 

        def generate_report_block(self, index):
            code = '''
            <tr>
                <td bgcolor="#3371ff"><b>Bloque Punteros '''+str(index)+'''</b></td>
            </tr>
            <tr>
                <td><b>b_pointers      </b> '''+str(self.b_pointers)+'''</td>
            </tr>'''
            return code
        
        def generate_report_tree(self, index):
            code = f'''
            pointer{index} [label=<<table cellspacing="0" cellpadding="2">
                <tr>
                    <td bgcolor="#3371ff"><b>Bloque Punteros{index}</b></td>
                </tr>'''
            for i in range(16):
                code += f'''
                <tr>
                    <td>{self.b_pointers[i]}</td>
                </tr>'''
            code += '''
            </table>>];
            '''
            return code