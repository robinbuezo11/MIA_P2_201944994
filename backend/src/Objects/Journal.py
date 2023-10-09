import ctypes
import struct
from Utils.Utilities import *

const = 'i50s100s19s'

class Journal(ctypes.Structure):

    _fields_ = [
        ('j_filesystem_op', ctypes.c_int), # 0 = MKDIR, 1 = MKFILE, 2 = RMDIR, 3 = RMFILE, 4 = EDIT, 5 = REN, 6 = MOVE, 7 = CAT, 8 = CHMOD, 9 = CHOWN, 10 = LOSS, 11 = RECOVERY
        ('j_path', ctypes.c_char * 50),
        ('j_content', ctypes.c_char * 100),
        ('j_date', ctypes.c_char * 19)
    ]

    def __init__(self):
        self.j_filesystem_op = -1
        self.j_path = b'\0'*50
        self.j_content = b'\0'*100
        self.j_date = b'\0'*19

    def get_const(self):
        return const
    
    def _set_j_filesystem_op(self, j_filesystem_op):
        self.j_filesystem_op = j_filesystem_op

    def _set_j_path(self, j_path):
        self.j_path = coding_str(j_path, 50)

    def _set_j_content(self, j_content):
        self.j_content = coding_str(j_content, 100)

    def _set_j_date(self, j_date):
        self.j_date = coding_str(j_date, 19)

    def set_info(self, j_filesystem_op, j_path, j_content, j_date):
        self._set_j_filesystem_op(j_filesystem_op)
        self._set_j_path(j_path)
        self._set_j_content(j_content)
        self._set_j_date(j_date)

    def display_info(self):
        print(f'j_filesystem_op: {self.j_filesystem_op}')
        print(f'j_path: {self.j_path.decode().replace(chr(0), "")}')
        print(f'j_content: {self.j_content.decode().replace(chr(0), "")}')
        print(f'j_date: {self.j_date.decode()}\n')

    def doSerialize(self):
        return struct.pack(
            const, 
            self.j_filesystem_op, 
            self.j_path, 
            self.j_content, 
            self.j_date)
    
    def doDeserialize(self, data):
        self.j_filesystem_op, self.j_path, self.j_content, self.j_date = struct.unpack(const, data)

    def generate_report_journal(self):
        operations = ['MKDIR', 'MKFILE', 'RMDIR', 'RMFILE', 'EDIT', 'REN', 'MOVE', 'CAT', 'CHMOD', 'CHOWN', 'LOSS', 'RECOVERY']
        return f'''
        <tr>
            <td>{operations[self.j_filesystem_op]}</td><td>{self.j_path.decode().replace(chr(0), "")}</td>
            <td>{self.j_content.decode().replace(chr(0), "")}</td><td>{self.j_date.decode()}</td>
        </tr>'''