import ctypes
import struct
import random
from Utils.Utilities import coding_str
from Objects.Partition import Partition
from Objects.EBR import EBR
from Utils.Fmanager import *

const = 'i19sis' 
#i es un entero de 4 bytes, 19s es un string de 19 bytes, i es un entero de 4 bytes, s es un string de 1 byte

class MBR(ctypes.Structure):

    _fields_ = [
        ('mbr_tamano', ctypes.c_int),
        ('mbr_fecha_creacion', ctypes.c_char * 19),
        ('mbr_dsk_signature', ctypes.c_int),
        ('dsk_fit', ctypes.c_char)
    ]

    def __init__(self):
        self.mbr_tamano = -1     # Tamaño del disco en KB
        self.mbr_fecha_creacion = b'\0'*19
        self.mbr_dsk_signature = -1
        self.dsk_fit = b'\0'
        self.partitions = [Partition(), Partition(), Partition(), Partition()]

    def get_const(self):
        return const
    
    def get_partitionbyName(self, name, file):
        for partition in self.partitions:
            if partition.part_type.decode() == 'e':
                ebr = EBR()
                if Fread_displacement(file, partition.part_start, ebr):
                    while ebr.part_next != -1:
                        if ebr.part_name.decode() == name:
                            return ebr
                        if Fread_displacement(file, ebr.part_next, ebr):
                            continue
                        else:
                            break
                    if ebr.part_name.decode() == name:
                        return ebr
                else:
                    break
            if partition.part_name.decode() == name:
                return partition
        return None
    
    def set_partitionbyName(self, name, partition, file):
        for partition in self.partitions:
            if partition.part_type.decode() == 'e':
                ebr = EBR()
                if Fread_displacement(file, partition.part_start, ebr):
                    while ebr.part_next != -1:
                        if ebr.part_name.decode() == name:
                            ebr = partition
                            return True
                        if Fread_displacement(file, ebr.part_next, ebr):
                            continue
                        else:
                            break
                    if ebr.part_name.decode() == name:
                        ebr = partition
                        return True
                else:
                    break
            elif partition.part_type.decode != 'e' and partition.part_name.decode() == name:
                partition = partition
                return True
        return False

    def _set_mbr_tamano(self, mbr_tamano):
        self.mbr_tamano = mbr_tamano

    def _set_mbr_fecha_creacion(self, mbr_fecha_creacion):
        self.mbr_fecha_creacion = coding_str(mbr_fecha_creacion, 19)

    def _set_mbr_dsk_signature(self, mbr_dsk_signature):
        self.mbr_dsk_signature = mbr_dsk_signature

    def _set_dsk_fit(self, dsk_fit):
        self.dsk_fit = coding_str(dsk_fit, 1)
 
    def set_info(self, mbr_fecha_creacion, mbr_tamano, dsk_fit):
        self._set_mbr_tamano(mbr_tamano)
        self._set_mbr_fecha_creacion(mbr_fecha_creacion)
        self._set_mbr_dsk_signature(random.randint(1, 2**31 - 1))
        self._set_dsk_fit(dsk_fit)
    
    def display_info(self):
        print("\n*** MBR ***")
        print(f"Tamaño: {self.mbr_tamano/1024} KB")
        print("Fecha de creacion: ", self.mbr_fecha_creacion.decode())
        print("Identificador: ", self.mbr_dsk_signature)
        print("Ajuste: ", self.dsk_fit.decode().upper())
        print("\n* PARTICIONES *")
        for i in range(4):
            print(f'Particion {i+1}:')
            if self.partitions[i].part_type == b'\0':
                print("No hay particion\n")
            else:
                self.partitions[i].display_info()

    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature,
            self.dsk_fit
        )
        for i in range(4):
            serialize += self.partitions[i].doSerialize()
        return serialize
    
    def doDeserialize(self, data):
        sizeMBR = struct.calcsize(const)
        sizePartition = struct.calcsize(Partition().get_const())

        dataMBR = data[:sizeMBR]
        self.mbr_tamano, self.mbr_fecha_creacion, self.mbr_dsk_signature, self.dsk_fit = struct.unpack(const, dataMBR)

        for i in range(4):
            dataPartition = data[sizeMBR + i*sizePartition: sizeMBR + (i+1)*sizePartition]
            self.partitions[i].doDeserialize(dataPartition)

    def generate_report_mbr(self, file):
        try:
            code = '''
            digraph G {
                node [shape=plain style=filled pencolor=black fontname="Helvetica, Arial, sans-serif"]
                mbr [label=<<table cellspacing="0" cellpadding="2">
                    <tr>
                        <td bgcolor="#3371ff"><b>MBR</b></td>
                    </tr>
                    <tr>
                        <td><b>mbr_tamano      </b> '''+str(self.mbr_tamano)+'''</td>
                    </tr>
                    <tr>
                        <td><b>mbr_fecha_creacion      </b> '''+self.mbr_fecha_creacion.decode()+'''</td>
                    </tr>
                    <tr>
                        <td><b>mbr_dsk_signature      </b> '''+str(self.mbr_dsk_signature)+'''</td>
                    </tr>
                    <tr>
                        <td><b>dsk_fit      </b> '''+self.dsk_fit.decode().upper()+'''</td>
                    </tr>'''
            for i in range(4):
                if self.partitions[i].part_s != -1:
                    code += self.partitions[i].generate_report_mbr(file)
            code += '''
                </table>>];
            }'''
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code
    
    def generate_report_disk(self, file, disk_name):
        try:
            code = '''
            digraph G {
                bgcolor="#3371ff" node [style=filled shape=record]
                disk [label="{''' + disk_name.upper() + '''|{MBR'''
            
            end_used = len(self.doSerialize())
            for partition in self.partitions:
                if partition.part_s != -1:
                    if end_used != partition.part_start:
                        code += f'|Libre\\n{(((partition.part_start - end_used)/self.mbr_tamano)*100):.2f}% del disco'
                    code += partition.generate_report_disk(file, self.mbr_tamano)
                    end_used = partition.part_start + partition.part_s
            if end_used != self.mbr_tamano:
                code += f'|Libre\\n{(((self.mbr_tamano - end_used)/self.mbr_tamano)*100):.2f}% del disco'
            code += '''}}"];
            }'''
        except Exception as e:
            print(f'Error al generar el reporte: {e}')
            code = ''
        return code