import ctypes
import struct
from Utils.Utilities import coding_str
from Utils.Fmanager import *
from Objects.Inode import Inode
from Objects.FileBlock import FileBlock
from Objects.FolderBlock import FolderBlock
from Objects.PointersBlock import PointersBlock
from Objects.Journaling import Journaling

const = 'iiiii19s19siHiiiiiiii'

class SuperBlock(ctypes.Structure):

    _fields_ = [
        ('s_filesystem_type', ctypes.c_int),
        ('s_inodes_count', ctypes.c_int),
        ('s_blocks_count', ctypes.c_int),
        ('s_free_blocks_count', ctypes.c_int),
        ('s_free_inodes_count', ctypes.c_int),
        ('s_mtime', ctypes.c_char * 19),
        ('s_umtime', ctypes.c_char * 19),
        ('s_mnt_count', ctypes.c_int),
        ('s_magic', ctypes.c_uint16),
        ('s_inode_s', ctypes.c_int),
        ('s_block_s', ctypes.c_int),
        ('s_first_ino', ctypes.c_int),
        ('s_first_blo', ctypes.c_int),
        ('s_bm_inode_start', ctypes.c_int),
        ('s_bm_block_start', ctypes.c_int),
        ('s_inode_start', ctypes.c_int),
        ('s_block_start', ctypes.c_int)
    ]

    def __init__(self):
        self.s_magic = 0xEF53

    def get_const(self):
        return const

    def _set_s_filesystem_type(self, s_filesystem_type):
        self.s_filesystem_type = s_filesystem_type

    def _set_s_inodes_count(self, s_inodes_count):
        self.s_inodes_count = s_inodes_count

    def _set_s_blocks_count(self, s_blocks_count):
        self.s_blocks_count = s_blocks_count

    def _set_s_free_blocks_count(self, s_free_blocks_count):
        self.s_free_blocks_count = s_free_blocks_count

    def _set_s_free_inodes_count(self, s_free_inodes_count):
        self.s_free_inodes_count = s_free_inodes_count

    def _set_s_mtime(self, s_mtime):
        self.s_mtime = coding_str(s_mtime, 19)

    def _set_s_umtime(self, s_umtime):
        self.s_umtime = coding_str(s_umtime, 19)

    def _set_s_mnt_count(self, s_mnt_count):
        self.s_mnt_count = s_mnt_count

    def _set_s_magic(self, s_magic):
        self.s_magic = s_magic

    def _set_s_inode_s(self, s_inode_s):
        self.s_inode_s = s_inode_s

    def _set_s_block_s(self, s_block_s):
        self.s_block_s = s_block_s

    def _set_s_first_ino(self, s_first_ino):
        self.s_first_ino = s_first_ino

    def _set_s_first_blo(self, s_first_blo):
        self.s_first_blo = s_first_blo

    def _set_s_bm_inode_start(self, s_bm_inode_start):
        self.s_bm_inode_start = s_bm_inode_start

    def _set_s_bm_block_start(self, s_bm_block_start):
        self.s_bm_block_start = s_bm_block_start

    def _set_s_inode_start(self, s_inode_start):
        self.s_inode_start = s_inode_start

    def _set_s_block_start(self, s_block_start):
        self.s_block_start = s_block_start
 
    def set_info(self, s_filesystem_type, s_inodes_count, s_blocks_count, s_free_blocks_count, s_free_inodes_count, s_mtime, s_umtime, 
                 s_mnt_count, s_magic, s_inode_s, s_block_s, s_first_ino, s_first_blo, s_bm_inode_start, s_bm_block_start, s_inode_start, s_block_start):
        self._set_s_filesystem_type(s_filesystem_type)
        self._set_s_inodes_count(s_inodes_count)
        self._set_s_blocks_count(s_blocks_count)
        self._set_s_free_blocks_count(s_free_blocks_count)
        self._set_s_free_inodes_count(s_free_inodes_count)
        self._set_s_mtime(s_mtime)
        self._set_s_umtime(s_umtime)
        self._set_s_mnt_count(s_mnt_count)
        self._set_s_magic(s_magic)
        self._set_s_inode_s(s_inode_s)
        self._set_s_block_s(s_block_s)
        self._set_s_first_ino(s_first_ino)
        self._set_s_first_blo(s_first_blo)
        self._set_s_bm_inode_start(s_bm_inode_start)
        self._set_s_bm_block_start(s_bm_block_start)
        self._set_s_inode_start(s_inode_start)
        self._set_s_block_start(s_block_start)
    
    def display_info(self):
        print("\n*** Super Bloque ***")
        print("Tipo de Sistema de Archivos: ", self.s_filesystem_type)
        print("Cantidad de Inodos: ", self.s_inodes_count)
        print("Cantidad de Bloques: ", self.s_blocks_count)
        print("Bloques Libres: ", self.s_free_blocks_count)
        print("Inodos Libres: ", self.s_free_inodes_count)
        print("Fecha de Montaje: ", self.s_mtime.decode())
        print("Ultima Fecha de Desmontaje: ", self.s_umtime.decode())
        print("Numero de Montajes: ", self.s_mnt_count)
        print("Magic Number: ", self.s_magic)
        print("Tamaño del Inodo: ", self.s_inode_s)
        print("Tamaño del Bloque: ", self.s_block_s)
        print("Primer Inodo Libre: ", self.s_first_ino)
        print("Primer Bloque Libre: ", self.s_first_blo)
        print("Inicio del Bitmap de Inodos: ", self.s_bm_inode_start)
        print("Inicio del Bitmap de Bloques: ", self.s_bm_block_start)
        print("Inicio de la Tabla de Inodos: ", self.s_inode_start)
        print("Inicio de la Tabla de Bloques: ", self.s_block_start, "\n")

    def doSerialize(self):
        return struct.pack(
            const,
            self.s_filesystem_type,
            self.s_inodes_count,
            self.s_blocks_count,
            self.s_free_blocks_count,
            self.s_free_inodes_count,
            self.s_mtime,
            self.s_umtime,
            self.s_mnt_count,
            self.s_magic,
            self.s_inode_s,
            self.s_block_s,
            self.s_first_ino,
            self.s_first_blo,
            self.s_bm_inode_start,
            self.s_bm_block_start,
            self.s_inode_start,
            self.s_block_start
        )
    
    def doDeserialize(self, data):
        (self.s_filesystem_type,
        self.s_inodes_count,
        self.s_blocks_count,
        self.s_free_blocks_count,
        self.s_free_inodes_count,
        self.s_mtime,
        self.s_umtime,
        self.s_mnt_count,
        self.s_magic,
        self.s_inode_s,
        self.s_block_s,
        self.s_first_ino,
        self.s_first_blo,
        self.s_bm_inode_start,
        self.s_bm_block_start,
        self.s_inode_start,
        self.s_block_start) = struct.unpack(const, data)

    def generate_report_inode(self, file):
        try:
            inode = Inode()
            code = ''
            connections = ''
            for i in range(self.s_inodes_count):
                Fread_displacement(file, self.s_inode_start + i * struct.calcsize(inode.get_const()), inode)
                if inode.i_s == -1:
                    continue

                code += f'node{i} [label = <<table cellspacing="0" cellpadding="2">\n'
                code += inode.generate_report_inode(i)
                code += '</table>>];\n'

                if i == 0:
                    connections += f'node{i}'
                else:
                    connections += f'->node{i}'
            code += connections + ';\n'
            return code
        except:
            return ''
        
    def generate_report_block(self, file):
        try:
            inode = Inode()
            block = None
            code = ''
            connections = ''
            first_block = True
            size_block = struct.calcsize(FileBlock().get_const())
            for i in range(self.s_inodes_count):
                Fread_displacement(file, self.s_inode_start + i * struct.calcsize(inode.get_const()), inode)
                if inode.i_s == -1:
                    continue

                if inode.i_type == b'1':
                    for i in range(12):
                        if inode.i_block[i] != -1:
                            block = FileBlock()
                            Fread_displacement(file, self.s_block_start + inode.i_block[i] * size_block, block)
                            code += f'node{inode.i_block[i]} [label = <<table cellspacing="0" cellpadding="2">\n'
                            code += block.generate_report_block(inode.i_block[i])
                            code += '</table>>];\n'
                            if first_block:
                                connections += f'node{inode.i_block[i]}'
                                first_block = False
                            else:
                                connections += f'->node{inode.i_block[i]}'
                    for i in range(3):
                        if inode.i_block[12+i] != -1:
                            block = PointersBlock()
                            Fread_displacement(file, self.s_block_start + inode.i_block[12+i] * size_block, block)
                            code += f'node{inode.i_block[12+i]} [label = <<table cellspacing="0" cellpadding="2">\n'
                            code += block.generate_report_block(inode.i_block[12+i])
                            code += '</table>>];\n'
                            if first_block:
                                connections += f'node{inode.i_block[12+i]}'
                                first_block = False
                            else:
                                connections += f'->node{inode.i_block[12+i]}'
                        if i == 1 and inode.i_block[12+i] != -1:
                            for j in range(16):
                                if block.b_pointers[j] != -1:
                                    block = PointersBlock()
                                    Fread_displacement(file, self.s_block_start + block.b_pointers[j] * size_block, block)
                                    code += f'node{block.b_pointers[j]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                    code += block.generate_report_block(block.b_pointers[j])
                                    code += '</table>>];\n'
                                    connections += f'->node{block.b_pointers[j]}'
                        if i == 2 and inode.i_block[12+i] != -1:
                            for j in range(16):
                                if block.b_pointers[j] != -1:
                                    block = PointersBlock()
                                    Fread_displacement(file, self.s_block_start + block.b_pointers[j] * size_block, block)
                                    code += f'node{block.b_pointers[j]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                    code += block.generate_report_block(block.b_pointers[j])
                                    code += '</table>>];\n'
                                    connections += f'->node{block.b_pointers[j]}'
                                    for k in range(16):
                                        if block.b_pointers[k] != -1:
                                            block = PointersBlock()
                                            Fread_displacement(file, self.s_block_start + block.b_pointers[k] * size_block, block)
                                            code += f'node{block.b_pointers[k]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                            code += block.generate_report_block(block.b_pointers[k])
                                            code += '</table>>];\n'
                                            connections += f'->node{block.b_pointers[k]}'
                elif inode.i_type == b'0':
                    for i in range(12):
                        if inode.i_block[i] != -1:
                            block = FolderBlock()
                            Fread_displacement(file, self.s_block_start + inode.i_block[i] * size_block, block)
                            code += f'node{inode.i_block[i]} [label = <<table cellspacing="0" cellpadding="2">\n'
                            code += block.generate_report_block(inode.i_block[i])
                            code += '</table>>];\n'
                            if first_block:
                                connections += f'node{inode.i_block[i]}'
                                first_block = False
                            else:
                                connections += f'->node{inode.i_block[i]}'
                    for i in range(3):
                        if inode.i_block[12+i] != -1:
                            block = PointersBlock()
                            Fread_displacement(file, self.s_block_start + inode.i_block[12+i] * size_block, block)
                            code += f'node{inode.i_block[12+i]} [label = <<table cellspacing="0" cellpadding="2">\n'
                            code += block.generate_report_block(inode.i_block[12+i])
                            code += '</table>>];\n'
                            if first_block:
                                connections += f'node{inode.i_block[12+i]}'
                                first_block = False
                            else:
                                connections += f'->node{inode.i_block[12+i]}'
                        if i == 1 and inode.i_block[12+i] != -1:
                            for j in range(16):
                                if block.b_pointers[j] != -1:
                                    block = PointersBlock()
                                    Fread_displacement(file, self.s_block_start + block.b_pointers[j] * size_block, block)
                                    code += f'node{block.b_pointers[j]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                    code += block.generate_report_block(block.b_pointers[j])
                                    code += '</table>>];\n'
                                    connections += f'->node{block.b_pointers[j]}'
                        if i == 2 and inode.i_block[12+i] != -1:
                            for j in range(16):
                                if block.b_pointers[j] != -1:
                                    block = PointersBlock()
                                    Fread_displacement(file, self.s_block_start + block.b_pointers[j] * size_block, block)
                                    code += f'node{block.b_pointers[j]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                    code += block.generate_report_block(block.b_pointers[j])
                                    code += '</table>>];\n'
                                    connections += f'->node{block.b_pointers[j]}'
                                    for k in range(16):
                                        if block.b_pointers[k] != -1:
                                            block = PointersBlock()
                                            Fread_displacement(file, self.s_block_start + block.b_pointers[k] * size_block, block)
                                            code += f'node{block.b_pointers[k]} [label = <<table cellspacing="0" cellpadding="2">\n'
                                            code += block.generate_report_block(block.b_pointers[k])
                                            code += '</table>>];\n'
                                            connections += f'->node{block.b_pointers[k]}'
            return code + connections + ';\n'
        except Exception as e:
            printError(f'Error al generar el reporte de bloques. {e}')
            return ''
        
    def generate_report_sb(self, file):
        try:            
            code = f'node_sb [label = <<table cellspacing="0" cellpadding="2">\n'
            code += '''
            <tr>
                <td bgcolor="#3371ff"><b>Super Bloque</b></td>
            </tr>
            <tr>
                <td><b>s_filesystem_type      </b> '''+str(self.s_filesystem_type)+'''</td>
            </tr>
            <tr>
                <td><b>s_inodes_count      </b> '''+str(self.s_inodes_count)+'''</td>
            </tr>
            <tr>
                <td><b>s_blocks_count      </b> '''+str(self.s_blocks_count)+'''</td>
            </tr>
            <tr>
                <td><b>s_free_blocks_count      </b> '''+str(self.s_free_blocks_count)+'''</td>
            </tr>
            <tr>
                <td><b>s_free_inodes_count      </b> '''+str(self.s_free_inodes_count)+'''</td>
            </tr>
            <tr>
                <td><b>s_mtime      </b> '''+self.s_mtime.decode()+'''</td>
            </tr>
            <tr>
                <td><b>s_umtime      </b> '''+self.s_umtime.decode()+'''</td>
            </tr>
            <tr>
                <td><b>s_mnt_count      </b> '''+str(self.s_mnt_count)+'''</td>
            </tr>
            <tr>
                <td><b>s_magic      </b> '''+str(self.s_magic)+'''</td>
            </tr>
            <tr>
                <td><b>s_inode_s      </b> '''+str(self.s_inode_s)+'''</td>
            </tr>
            <tr>
                <td><b>s_block_s      </b> '''+str(self.s_block_s)+'''</td>
            </tr>
            <tr>
                <td><b>s_first_ino      </b> '''+str(self.s_first_ino)+'''</td>
            </tr>
            <tr>
                <td><b>s_first_blo      </b> '''+str(self.s_first_blo)+'''</td>
            </tr>
            <tr>
                <td><b>s_bm_inode_start      </b> '''+str(self.s_bm_inode_start)+'''</td>
            </tr>
            <tr>
                <td><b>s_bm_block_start      </b> '''+str(self.s_bm_block_start)+'''</td>
            </tr>
            <tr>
                <td><b>s_inode_start      </b> '''+str(self.s_inode_start)+'''</td>
            </tr>
            <tr>
                <td><b>s_block_start      </b> '''+str(self.s_block_start)+'''</td>
            </tr>
            '''
            code += '</table>>];\n'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_tree(self, file):
        try:
            inode = Inode()
            code = ''
            connections = ''
            index = 0
            for i in range(self.s_inodes_count):
                Fread_displacement(file, self.s_inode_start + i * struct.calcsize(inode.get_const()), inode)
                if inode.i_s != -1:
                    index = i
                    break
            code, connections = self.graph_tree([None,None], inode, file, index)
        except Exception as e:
            printError(f'Error al generar el reporte de arbol. {e}')
            code = ''
        return code + connections + '\n'

    def graph_tree(self, parent, obj, file, index):
        code = ''
        connections = ''
        block_size = struct.calcsize(FileBlock().get_const())
        if obj== None:
            return '', ''
        
        if isinstance(obj, Inode):
            code += obj.generate_report_tree(index)
            if parent[0] != None:
                if isinstance(parent[0], Inode):
                    connections += f'inode{parent[1]}->inode{index};\n'
                elif isinstance(parent[0], FolderBlock):
                    connections += f'folder{parent[1]}->inode{index};\n'
                elif isinstance(parent[0], FileBlock):
                    connections += f'file{parent[1]}->inode{index};\n'
                elif isinstance(parent[0], PointersBlock):
                    connections += f'pointers{parent[1]}->inode{index};\n'
            
            if obj.i_type == b'0':
                for i in range(12):
                    if obj.i_block[i] != -1:
                        block = FolderBlock()
                        Fread_displacement(file, self.s_block_start + obj.i_block[i] * block_size, block)
                        newcode, newconnections = self.graph_tree([obj,index], block, file, obj.i_block[i])
                        code += newcode
                        connections += newconnections
            if obj.i_type == b'1':
                for i in range(12):
                    if obj.i_block[i] != -1:
                        block = FileBlock()
                        Fread_displacement(file, self.s_block_start + obj.i_block[i] * block_size, block)
                        newcode, newconnections = self.graph_tree([obj,index], block, file, obj.i_block[i])
                        code += newcode
                        connections += newconnections
            for i in range(12, 15):
                if obj.i_block[i] != -1:
                    block = PointersBlock()
                    Fread_displacement(file, self.s_block_start + obj.i_block[i] * block_size, block)
                    newcode, newconnections = self.graph_tree([obj,index], block, file, obj.i_block[i])
                    code += newcode
                    connections += newconnections
            
        elif isinstance(obj, FileBlock):
            code += obj.generate_report_tree(index)
            if parent[0] != None:
                if isinstance(parent[0], Inode):
                    connections += f'inode{parent[1]}->file{index};\n'
                elif isinstance(parent[0], FolderBlock):
                    connections += f'folder{parent[1]}->file{index};\n'
                elif isinstance(parent[0], FileBlock):
                    connections += f'file{parent[1]}->file{index};\n'
                elif isinstance(parent[0], PointersBlock):
                    connections += f'pointers{parent[1]}->file{index};\n'
        elif isinstance(obj, FolderBlock):
            code += obj.generate_report_tree(index)
            if parent[0] != None:
                if isinstance(parent[0], Inode):
                    connections += f'inode{parent[1]}->folder{index};\n'
                elif isinstance(parent[0], FolderBlock):
                    connections += f'folder{parent[1]}->folder{index};\n'
                elif isinstance(parent[0], FileBlock):
                    connections += f'file{parent[1]}->folder{index};\n'
                elif isinstance(parent[0], PointersBlock):
                    connections += f'pointers{parent[1]}->folder{index};\n'
            for i in range(2,4):
                if obj.b_content[i].b_inodo != -1:
                    inode = Inode()
                    Fread_displacement(file, self.s_inode_start + obj.b_content[i].b_inodo * struct.calcsize(inode.get_const()), inode)
                    newcode, newconnections = self.graph_tree([obj,index], inode, file, obj.b_content[i].b_inodo)
                    code += newcode
                    connections += newconnections
        elif isinstance(obj, PointersBlock):
            code += obj.generate_report_tree(index)
            if parent[0] != None:
                if isinstance(parent[0], Inode):
                    connections += f'inode{parent[1]}->pointer{index};\n'
                elif isinstance(parent[0], FolderBlock):
                    connections += f'folder{parent[1]}->pointer{index};\n'
                elif isinstance(parent[0], FileBlock):
                    connections += f'file{parent[1]}->pointer{index};\n'
                elif isinstance(parent[0], PointersBlock):
                    connections += f'pointers{parent[1]}->pointer{index};\n'
            for i in range(16):
                if obj.b_pointers[i] != -1:
                    block = PointersBlock()
                    Fread_displacement(file, self.s_block_start + obj.b_pointers[i] * block_size, block)
                    newcode, newconnections = self.graph_tree([obj,index], block, file, obj.b_pointers[i])
                    code += newcode
                    connections += newconnections
        
        return code, connections
    
    def generate_report_file(self, file, path):
        if path[0] == '/':
            path = '.' + path

        if path[0:2] != './':
            path = './' + path

        try:
            inode = Inode()
            code = ''
            path = path.split('/')
            current_folder = FolderBlock()
            size_block = struct.calcsize(FileBlock().get_const())
            # Get the root folder
            folder_name = path.pop(0)
            found = False
            for i in range(self.s_inodes_count):
                Fread_displacement(file, self.s_inode_start + i * struct.calcsize(inode.get_const()), inode)
                if inode.i_type == b'0' and inode.i_s != -1:
                    block = FolderBlock()
                    Fread_displacement(file, self.s_block_start + inode.i_block[0] * size_block, block)
                    for j in range(4):
                        if block.b_content[j].b_name.decode() == folder_name:
                            current_folder = block
                            found = True
                            break
                if found:
                    break

            # Get the folder where the file is
            while len(path) > 1:
                folder_name = path.pop(0)
                found = False
                for i in range(4):
                    if current_folder.b_content[i].b_name.decode() == folder_name:
                        inode = Inode()
                        Fread_displacement(file, self.s_inode_start + current_folder.b_content[i].b_inodo * struct.calcsize(inode.get_const()), inode)
                        block = FolderBlock()
                        Fread_displacement(file, self.s_block_start + inode.i_block[0] * size_block, block)
                        current_folder = block
                        found = True
                        break
                if not found:
                    printError(f'No se encontro el directorio {folder_name}')
                    return ''
                
            # Get the file
            file_name = path.pop(0)
            for i in range(4):
                if current_folder.b_content[i].b_name.decode() == file_name:
                    inode = Inode()
                    Fread_displacement(file, self.s_inode_start + current_folder.b_content[i].b_inodo * struct.calcsize(inode.get_const()), inode)
                    block = FileBlock()
                    code += f'Nombre: {file_name}\nContenido:'
                    for j in range(12):
                        if inode.i_block[j] != -1:
                            Fread_displacement(file, self.s_block_start + inode.i_block[j] * size_block, block)
                            code += block.b_content.decode()
                            break
                    return code
        except Exception as e:
            printError(f'Error al generar el reporte de archivo. {e}')
            return ''
        