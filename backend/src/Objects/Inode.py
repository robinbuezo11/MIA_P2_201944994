import ctypes
import struct
from Utils.Utilities import coding_str
from Utils.Fmanager import *
from Objects.FileBlock import FileBlock
from Objects.FolderBlock import FolderBlock
from Objects.PointersBlock import PointersBlock

const = 'iii19s19s19s15isi'

class Inode(ctypes.Structure):

    _fields_ = [
        ('i_uid', ctypes.c_int),
        ('i_gid', ctypes.c_int),
        ('i_s', ctypes.c_int),
        ('i_atime', ctypes.c_char * 19),
        ('i_ctime', ctypes.c_char * 19),
        ('i_mtime', ctypes.c_char * 19),
        ('i_block', ctypes.c_int * 15),
        ('i_type', ctypes.c_char),
        ('i_perm', ctypes.c_int)
    ]

    def __init__(self):
        self.i_uid = -1
        self.i_gid = -1
        self.i_s = -1
        self.i_atime = b'\0'*19
        self.i_ctime = b'\0'*19
        self.i_mtime = b'\0'*19
        self.i_block = (ctypes.c_int * 15)(*[-1]*15)
        self.i_type = b'\0'
        self.i_perm = -1

    def get_const(self):
        return const

    def _set_i_uid(self, i_uid):
        self.i_uid = i_uid

    def _set_i_gid(self, i_gid):
        self.i_gid = i_gid

    def _set_i_s(self, i_s):
        self.i_s = i_s

    def _set_i_atime(self, i_atime):
        self.i_atime = coding_str(i_atime, 19)

    def _set_i_ctime(self, i_ctime):
        self.i_ctime = coding_str(i_ctime, 19)

    def _set_i_mtime(self, i_mtime):
        self.i_mtime = coding_str(i_mtime, 19)

    def _set_i_block(self, i_block):
        self.i_block = i_block

    def _set_i_type(self, i_type):
        self.i_type = coding_str(i_type, 1)

    def _set_i_perm(self, i_perm):
        self.i_perm = i_perm

    def set_info(self, i_uid, i_gid, i_s, i_atime, i_ctime, i_mtime, i_block, i_type, i_perm):
        self._set_i_uid(i_uid)
        self._set_i_gid(i_gid)
        self._set_i_s(i_s)
        self._set_i_atime(i_atime)
        self._set_i_ctime(i_ctime)
        self._set_i_mtime(i_mtime)
        self._set_i_block(i_block)
        self._set_i_type(i_type)
        self._set_i_perm(i_perm)

    def display_info(self):
        print("\n*** Tabla de Inodos ***")
        print("UID: ", self.i_uid)
        print("GID: ", self.i_gid)
        print("Tamaño: ", self.i_s)
        print("Fecha de acceso: ", self.i_atime.decode().upper())
        print("Fecha de creación: ", self.i_ctime.decode().upper())
        print("Fecha de modificación: ", self.i_mtime.decode().upper())
        print("Bloques: ", list(self.i_block))
        print("Tipo: ", self.i_type.decode().upper())
        print("Permisos: ", self.i_perm, "\n")

    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.i_uid,
            self.i_gid,
            self.i_s,
            self.i_atime,
            self.i_ctime,
            self.i_mtime,
            *self.i_block,
            self.i_type,
            self.i_perm
        )
        return serialize
    
    def doDeserialize(self, data):
        unpack = struct.unpack(const, data)
        (
            self.i_uid,
            self.i_gid,
            self.i_s,
            self.i_atime,
            self.i_ctime,
            self.i_mtime,
        ) = unpack[:6]

        self.i_block = (ctypes.c_int * 15)(*unpack[6:21])

        (
            self.i_type,
            self.i_perm
        ) = unpack[21:]

    def generate_report_inode(self, index):
        code = '''<tr>
                    <td bgcolor="#3371ff"><b>Inodo '''+str(index)+'''</b></td>
                </tr>
                <tr>
                    <td><b>i_uid      </b> '''+str(self.i_uid)+'''</td>
                </tr>
                <tr>
                    <td><b>i_gid      </b> '''+str(self.i_gid)+'''</td>
                </tr>
                <tr>
                    <td><b>i_size      </b> '''+str(self.i_s)+'''</td>
                </tr>
                <tr>
                    <td><b>i_atime      </b> '''+self.i_atime.decode()+'''</td>
                </tr>
                <tr>
                    <td><b>i_ctime      </b> '''+self.i_ctime.decode()+'''</td>
                </tr>
                <tr>
                    <td><b>i_mtime      </b> '''+self.i_mtime.decode()+'''</td>
                </tr>
                <tr>
                    <td><b>i_block      </b> '''+str(list(self.i_block))+'''</td>
                </tr>
                <tr>
                    <td><b>i_type      </b> '''+self.i_type.decode()+'''</td>
                </tr>
                <tr>
                    <td><b>i_perm      </b> '''+str(self.i_perm)+'''</td>
                </tr>'''
        return code
    
    def generate_report_tree(self, index):
        try:
            code = f'''
            inode{index} [label=<<table cellspacing="0" cellpadding="2">
                <tr>
                    <td bgcolor="#3371ff"><b>Inodo{index}</b></td>
                </tr>
                <tr>
                    <td><b>i_uid      </b> {self.i_uid}</td>
                </tr>
                <tr>
                    <td><b>i_gid      </b> {self.i_gid}</td>
                </tr>
                <tr>
                    <td><b>i_size      </b> {self.i_s}</td>
                </tr>
                <tr>
                    <td><b>i_atime      </b> {self.i_atime.decode()}</td>
                </tr>
                <tr>
                    <td><b>i_ctime      </b> {self.i_ctime.decode()}</td>
                </tr>
                <tr>
                    <td><b>i_mtime      </b> {self.i_mtime.decode()}</td>
                </tr>'''
            for i in range(15):
                code += f'''
                <tr>
                    <td><b>i_block[{i}]      </b> {self.i_block[i]}</td>
                </tr>'''
            code += f'''
                <tr>
                    <td><b>i_type      </b> {self.i_type.decode()}</td>
                </tr>
                <tr>
                    <td><b>i_perm      </b> {self.i_perm}</td>
                </tr>
            </table>>];'''
                        
        except Exception as e:
            print(f'Error al generar reporte tree: {e}')
            return '', ''
        return code