import ctypes
import struct
from Objects.Content import Content

class FolderBlock(ctypes.Structure):

    def __init__(self):
        self.b_content = [Content(),Content(),Content(),Content()]

    def display_info(self):
        print("\nBloque de Carpeta")
        for i in range(4):
            print("Content", i)
            self.b_content[i].display_info()
    
    def doSerialize(self): 
        serialize = b''
        for i in range(4):
            serialize += self.b_content[i].doSerialize()
        return serialize

    def doDeserialize(self, data):
        sizeContent = struct.calcsize(Content().getConst())

        for i in range(4):
            dataContent = data[i*sizeContent: (i+1)*sizeContent]
            self.b_content[i].doDeserialize(dataContent)
            
    def generate_report_block(self, index):
        code = '''
        <tr>
            <td bgcolor="#3371ff"><b>Bloque Carpeta '''+str(index)+'''</b></td>
        </tr>'''
        for i in range(4):
            code += self.b_content[i].generate_report_block()
        return code

    def generate_report_tree(self, index):
        code = f'''
        folder{index} [label=<<table cellspacing="0" cellpadding="2">
            <tr>
                <td bgcolor="#3371ff"><b>Bloque Carpeta{index}</b></td><td bgcolor="#3371ff"><b>P</b></td>
            </tr>
        '''
        for i in range(4):
            code += self.b_content[i].generate_report_tree()
        code += '''
        </table>>];
        '''
        return code
