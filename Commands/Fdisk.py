from Utils.load import *
from Objects.Partition import Partition
from Objects.MBR import MBR

def fdisk(path, size, unit, name):
    print('Ejecutando el comando FDISK')
    print("=====Abriendo Disco======")
    file = open(path, "rb+")
    mbr = MBR()
    Fread_displacement(file, 0, mbr)
    cursor = file.tell()
    for i in range(4):
        part = Fread_displacement(file, cursor, Partition())
        if part:
            cursor += part.part_s * 1024
        else:
            break

    if unit == 'M':
        size = size * 1024
    elif unit == 'B':
        size = size / 1024

    print("=====Creando PARTICIÓN======")

    part = Partition()
    part.set_info('Y', 'P', 'W', cursor, size, name)
    part.display_info()

    print("=====Escribiendo PARTICIÓN======")
    Fwrite_displacement(file, cursor, part)
    file.close()

    print("=====Finalizando FDISK======")