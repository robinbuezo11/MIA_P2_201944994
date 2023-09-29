from Utils.Utilities import *

def execute(path):
    printConsole(f'Ejecutando el comando EXECUTE\n')
    try:
        file = open(path, 'r')
        data = file.read()
        return data
    except:
        printError(f'No se pudo abrir el archivo {path}')
        return ''