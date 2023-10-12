import os
import struct
from Objects.MBR import MBR
from datetime import datetime
from Utils.Fmanager import *
from Utils.Utilities import *

def mkdisk(path, size, unit, fit):
    result = 'Ejecutando el comando MKDISK\n'
    result += '\n***** Creando MBR *****\n'

    size_bytes = get_sizeB(size, unit)

    fit = fit[0]

    mbr = MBR()
    mbr.set_info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), size_bytes, fit)
    result += mbr.display_info()

    result += "\n***** Creando Disco *****\n"
    directory, file_name = os.path.split(path)
    if directory != '':
        if not os.path.exists(directory):
            os.makedirs(directory)

    res, msg = Fcreate_file(path)
    if res:
        result += f'Se creo el disco {file_name} en {directory}\n'
    else:
        result += msg + f'No se pudo crear el disco {file_name} en {directory}\n'
        return result

    try:
        file = open(path, "rb+")
    except Exception as e:
        result += f"{e}\n"
        return result

    result += "\n***** Aplicando Tamaño *****\n"
    mb = get_sizeM(size_bytes, 'b')

    res, msg = Winit_size(file, mb)
    if res:
        result += f'Se aplico el tamaño {mb}MB al disco {file_name}\n'
    else:
        result += msg + f'No se pudo aplicar el tamaño al disco {file_name}\n'
        file.close()
        return result
    
    if struct.calcsize(mbr.get_const()) > size_bytes:
        result += f'El tamaño del disco es muy pequeño para el MBR\n'
        file.close()
        return result

    result += "\n***** Escribiendo MBR *****\n"
    res, msg = Fwrite_displacement(file, 0, mbr)
    if res:
        result += "Se escribio el MBR correctamente\n"
    else:
        result += msg + "No se pudo escribir el MBR\n"
    
    try:
        file.close()
    except Exception as e:
        result += f"{e}\n"
        return result
    
    result += "\nFinalizando MKDISK\n\n"
    return result