from Utils.Utilities import *
from Utils.Fmanager import *

def rmdisk(path):
    result = 'Ejecutando el comando RMDISK\n'

    # if not printWarning("Esta seguro que desea eliminar el disco? (s/n)"):
        # printConsole("Finalizando RMDISK\n")
        # return False

    result += "\n***** Eliminando Disco *****\n"

    res, msg = Fdelete_file(path)
    if res:
        result += f'Se elimino el disco {path}\n'
    else:
        result += msg + f'No se pudo eliminar el disco {path}\n'

    result += "\nFinalizando RMDISK\n\n"
    return result