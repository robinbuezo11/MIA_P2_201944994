from Utils.Utilities import *
from Utils.Fmanager import *

def rmdisk(path):
    printConsole('Ejecutando el comando RMDISK')

    if not printWarning("Esta seguro que desea eliminar el disco? (s/n)"):
        printConsole("Finalizando RMDISK\n")
        return False

    print("***** Eliminando Disco *****")

    if Fdelete_file(path):
        printSuccess(f'Se elimino el disco {path}')
    else:
        printError(f'No se pudo eliminar el disco {path}')

    printConsole("Finalizando RMDISK\n")
    return True