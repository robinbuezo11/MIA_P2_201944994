import os
import struct
from Objects.MBR import MBR
from datetime import datetime
from Utils.Fmanager import *
from Utils.Utilities import *

def mkdisk(path, size, unit, fit):
    printConsole('Ejecutando el comando MKDISK')
    print("***** Creando MBR *****")

    size_bytes = get_sizeB(size, unit)

    fit = fit[0]

    mbr = MBR()
    mbr.set_info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), size_bytes, fit)
    mbr.display_info()

    print("\n***** Creando Disco *****")
    directory, file_name = os.path.split(path)
    if directory != '':
        if not os.path.exists(directory):
            os.makedirs(directory)

    if Fcreate_file(path):
        printSuccess(f'Se creo el disco {file_name} en {directory}')
    else:
        printError(f'No se pudo crear el disco {file_name} en {directory}')
        return False

    try:
        file = open(path, "rb+")
    except Exception as e:
        printError(f"{e}")
        return False

    print("\n***** Aplicando Tamaño *****")
    mb = get_sizeM(size_bytes, 'b')
    if Winit_size(file, mb):
        printSuccess(f'Se aplico el tamaño {mb}MB al disco {file_name}')
    else:
        printError(f'No se pudo aplicar el tamaño al disco {file_name}')
        file.close()
        return False
    
    if struct.calcsize(mbr.get_const()) > size_bytes:
        printError(f'El tamaño del disco es muy pequeño para el MBR')
        file.close()
        return False

    print("\n***** Escribiendo MBR *****")
    if Fwrite_displacement(file, 0, mbr):
        printSuccess("Se escribio el MBR correctamente")
    else:
        printError("No se pudo escribir el MBR")
    
    try:
        file.close()
    except Exception as e:
        printError(f"{e}")
        return False
    
    printConsole("Finalizando MKDISK\n")
    return True