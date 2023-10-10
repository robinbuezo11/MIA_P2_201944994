import os
import struct
from Objects.MBR import MBR
from datetime import datetime
from Utils.Fmanager import *
from Utils.Utilities import *

def mkdisk(path, size, unit, fit):
    result = 'Ejecutando el comando MKDISK\n'
    result += '***** Creando MBR *****\n'

    size_bytes = get_sizeB(size, unit)

    fit = fit[0]

    mbr = MBR()
    mbr.set_info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), size_bytes, fit)
    result += mbr.display_info()

    print("\n***** Creando Disco *****")
    directory, file_name = os.path.split(path)
    if directory != '':
        if not os.path.exists(directory):
            os.makedirs(directory)

    if Fcreate_file(path):
        result += f'Se creo el disco {file_name} en {directory}\n'
    else:
        printError(f'No se pudo crear el disco {file_name} en {directory}')
        result += f'No se pudo crear el disco {file_name} en {directory}\n'
        return result

    try:
        file = open(path, "rb+")
    except Exception as e:
        result += f"{e}\n"
        return result

    result += "\n***** Aplicando Tamaño *****\n"
    mb = get_sizeM(size_bytes, 'b')
    if Winit_size(file, mb):
        result += f'Se aplico el tamaño {mb}MB al disco {file_name}\n'
    else:
        result += f'No se pudo aplicar el tamaño al disco {file_name}\n'
        file.close()
        return result
    
    if struct.calcsize(mbr.get_const()) > size_bytes:
        result += f'El tamaño del disco es muy pequeño para el MBR\n'
        file.close()
        return result

    result += "\n***** Escribiendo MBR *****\n"
    if Fwrite_displacement(file, 0, mbr):
        result += "Se escribio el MBR correctamente\n"
    else:
        result += "No se pudo escribir el MBR\n"
    
    try:
        file.close()
    except Exception as e:
        result += f"{e}\n"
        return result
    
    result += "\nFinalizando MKDISK\n"
    return result