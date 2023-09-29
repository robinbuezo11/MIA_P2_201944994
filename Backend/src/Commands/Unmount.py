from Utils.Utilities import *
from Utils.Globals import *

def unmount(id):
    printConsole('Ejecutando el comando UNMOUNT')
    print('\n***** Buscando la particion *****')
    partition = get_mounted_partitionbyId(id)
    if not partition:
        printError(f'No se encontro la particion {id} entre las particiones montadas')
        return False

    print('\n***** Desmontando la particion *****')
    mounted_partitions.remove(partition)
    printSuccess(f'Particion {id} desmontada con exito')
    display_mounted_partitions()
    printConsole('Finalizando UNMOUNT\n')