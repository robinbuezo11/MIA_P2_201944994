import os
import random
from Objects.MBR import MBR
from datetime import datetime
from Utils.load import *

def mkdisk(path, size, unit):
    print('Ejecutando el comando MKDISK')
    print("=====Creando MBR======")

    if unit == 'M':
        size = size * 1024

    mbr = MBR()
    mbr.set_info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), size)
    mbr.display_info()

    directory, file_name = os.path.split(path)

    if directory != '':
        if not os.path.exists(directory):
            os.makedirs(directory)

    print("=====Creando Disco======")
    if Fcreate_file(path): return

    file = open(path, "rb+")

    print("=====Aplicando Tamaño======")
    mb = int(mbr.mbr_tamano / 1024)
    Winit_size(file, mb)


    print("=====Writing MBR======")
    Fwrite_displacement(file, 0, mbr)
    file.close()
    print("=====Finalizando MKDISK======")

    return True