import ctypes
import struct
from Utils.Utilities import coding_str
from Utils.Fmanager import *
from Objects.EBR import EBR
from Objects.SuperBlock import SuperBlock
from Objects.Journaling import Journaling


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
        self.part_start = -1
        self.part_s = -1
        self.part_name = b'\0'*16

    def get_const(self):
        return const

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
        print("Estado: ", self.part_status.decode().upper())
        print("Tipo: ", self.part_type.decode().upper())
        print("Ajuste: ", self.part_fit.decode().upper())
        print("Inicio: ", self.part_start)
        print(f"Tamaño: {self.part_s/1024} KB")
        print("Nombre: ", self.part_name.decode().upper(), "\n")

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

    def generate_report_mbr(self, file):
        code = '''
            <tr>
                <td bgcolor="#3371ff"><b>MBR</b></td>
            </tr>
            <tr>
                <td><b>part_status      </b> ''' + self.part_status.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_type      </b> ''' + self.part_type.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_fit      </b> ''' + self.part_fit.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_start      </b> ''' + str(self.part_start) + '''</td>
            </tr>
            <tr>
                <td><b>part_size      </b> ''' + str(self.part_s) + '''</td>
            </tr>
            <tr>
                <td><b>part_name      </b> ''' + self.part_name.decode().upper() + '''</td>
            </tr>
            '''
        if self.part_type.decode() == 'e':
            ebr = EBR()
            if not Fread_displacement(file, self.part_start, ebr):
                printError(f'No se pudo leer el EBR del disco {file.name}')
                return code
            if ebr.part_s != -1:
                code += ebr.generate_report_mbr()
            while ebr.part_next != -1:
                if not Fread_displacement(file, ebr.part_next, ebr):
                    printError(f'No se pudo leer el EBR del disco {file.name}')
                    return code
                if ebr.part_s != -1:
                    code += ebr.generate_report_mbr()
        return code
    
    def generate_report_disk(self, file, size_disk):
        if self.part_type.decode() == 'e':
            ebr = EBR()
            ebrsize = struct.calcsize(ebr.get_const())
            if not Fread_displacement(file, self.part_start, ebr):
                printError(f'No se pudo leer el EBR del disco {file.name}')
                return ''
            end_used = self.part_start
            code = '''|{Extendida|{'''
            while ebr.part_next != -1:
                if end_used != ebr.part_start - ebrsize:
                    code += f'Libre\\n{((((ebr.part_start-ebrsize) - end_used)/size_disk)*100):.2f}% del disco|'
                code += f'EBR|Lógica\\n{(((ebr.part_s)/size_disk)*100):.2f}% del disco|'
                end_used = ebr.part_start + ebr.part_s

                if not Fread_displacement(file, ebr.part_next, ebr):
                    printError(f'No se pudo leer el EBR del disco {file.name}')
                    return ''
            if ebr.part_s != -1:
                if end_used != ebr.part_start - ebrsize:
                    code += f'Libre\\n{((((ebr.part_start-ebrsize) - end_used)/size_disk)*100):.2f}% del disco'
                code += f'EBR|Lógica\\n{(((ebr.part_s)/size_disk)*100):.2f}% del disco'
                end_used = ebr.part_start + ebr.part_s
                
            if end_used != self.part_start + self.part_s:
                code += f'|Libre\\n{(((self.part_start + self.part_s - end_used)/size_disk)*100):.2f}% del disco'
            code += '''}}'''
            return code
        else:
            code = f'|Primaria\\n{(((self.part_s)/size_disk)*100):.2f}% del disco'
            return code
        
    def generate_report_inode(self, file):
        try:
            code = '''
            digraph G {
            rankdir="LR"
                subgraph inod {
                    bgcolor="#3371ff" node [style=filled shape=record]'''
            
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return code + '''inode [label = "No se pudo leer el Super Bloque"];}'''
            
            code += super_block.generate_report_inode(file)
            code += '}\n}'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code

    def generate_report_block(self, file):
        try:
            code = '''
            digraph G {
            rankdir="LR"
                subgraph block {
                    bgcolor="#3371ff" node [style=filled shape=record]'''
            
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return code + '''block [label = "No se pudo leer el Super Bloque"];}'''
            
            code += super_block.generate_report_block(file)
            code += '}\n}'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_bm_inode(self, file):
        try:
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return ''
            
            code = Fread_displacement_data(file, super_block.s_bm_inode_start, super_block.s_inodes_count)
            code = code.decode()
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_bm_block(self, file):
        try:
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return ''
            
            code = Fread_displacement_data(file, super_block.s_bm_block_start, super_block.s_blocks_count)
            code = code.decode()
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_tree(self, file):
        try:
            code = '''
            digraph G {
            rankdir="LR"
                subgraph tree {
                    bgcolor="#3371ff" node [style=filled shape=record]'''
            
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return code + '''tree [label = "No se pudo leer el Super Bloque"];}'''
            
            code += super_block.generate_report_tree(file)
            code += '}\n}'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_sb(self, file):
        try:
            code = '''
            digraph G {
            rankdir="LR"
                subgraph sb {
                    bgcolor="#3371ff" node [style=filled shape=record] '''
            
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return code + '''sb [label = "No se pudo leer el Super Bloque"];}\n}'''
            code += super_block.generate_report_sb(file)
            code += '}\n}'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_file(self, file, path):
        try:
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return ''
            
            code = super_block.generate_report_file(file, path)
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_ls(self, file):
        return ''
    
    def generate_report_journaling(self, file):
        try:
            code = '''
            digraph G {
            rankdir="LR"
                subgraph journaling {
                    bgcolor="#3371ff" node [style=filled shape=record]'''
            
            super_block = SuperBlock()
            if not Fread_displacement(file, self.part_start, super_block):
                printError(f'No se pudo leer el Super Bloque del disco {file.name}')
                return code + '''journaling [label = "No se pudo leer el Super Bloque"];}\n}'''
            
            if super_block.s_filesystem_type == 2:
                printError(f'El sistema de archivos del disco {file.name} no es EXT3')
                return code + '''journaling [label = "El sistema de archivos no es EXT3"];}\n}'''
            
            journaling = Journaling()
            if not Fread_displacement(file, self.part_start + struct.calcsize(super_block.get_const()), journaling):
                printError(f'No se pudo leer el Journaling del disco {file.name}')
                return code + '''journaling [label = "No se pudo leer el Journaling"];}\n}'''
            

            code += journaling.generate_report_journaling()
            code += '}\n}'
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code