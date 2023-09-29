from Utils.Utilities import *
from Utils.Fmanager import *
from Objects.MBR import *
from Utils.Globals import *

def mount(path, name):
    printConsole('Ejecutando el comando MOUNT')
    print('\n***** Abriendo el disco *****')
    try:
        file = open(path, 'rb+')
    except:
        printError(f'No se pudo abrir el disco {path}')
        return False
    
    print('\n***** Leyendo el MBR *****')
    mbr = MBR()
    if not Fread_displacement(file, 0, mbr):
        printError(f'No se pudo leer el MBR del disco {path}')
        file.close()
        return False    
    mbr.display_info()
    
    print('\n***** Buscando la particion *****')
    partition = mbr.get_partitionbyName(name, file)
    if not partition:
        printError(f'No se encontro la particion {name} en el disco {path}')
        file.close()
        return False
    
    if not isinstance(partition, EBR):
        if partition.part_type.decode() == 'e':
            printError(f'No se puede montar una particion extendida')
            file.close()
            return False

    if partition.part_status.decode() == 'y':
        printError(f'La particion {name} ya esta montada')
        file.close()
        return False
    
    partition.display_info()
    # We make the id of the partition
    print('\n***** Creando ID de la particion *****')
    _, disk_name = os.path.split(path)
    disk_name = disk_name[:-4]

    index = 1
    for data in mounted_partitions:
        if data['path'] == path:
            index = int(data['id'][2:3]) + 1

    id = '94' + str(index) + disk_name
    print(f'ID: {id}')

    # We add the partition to the list
    print('\n***** Montando la partición *****')
    partition.part_status = b'y'
    if not mbr.set_partitionbyName(name, partition, file):
        printError(f'No se pudo montar la particion {name} del disco {path}')
        file.close()
        return False
    
    if not Fwrite_displacement(file, 0, mbr):
        printError(f'No se pudo escribir el MBR del disco {path}')
        file.close()
        return False
    
    mounted_partitions.append({'id': id, 'path': path, 'name': name, 'partition': partition})
    
    try:
        file.close()
    except:
        printError(f'No se pudo cerrar el disco {path}')
        return False
    
    printSuccess(f'Particion {name} montada con exito')
    display_mounted_partitions()
    printConsole('Finalizando MOUNT\n')