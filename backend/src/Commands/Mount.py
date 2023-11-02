from Utils.Utilities import *
from Utils.Fmanager import *
from Objects.MBR import *
from Utils.Globals import *

def mount(path, name):
    result = "Ejecutando el comando MOUNT\n"
    result += "\n***** Abriendo el disco *****\n"
    try:
        file = open(path, 'rb+')
    except:
        result += f'No se pudo abrir el disco {path}\n'
        return result
    
    result += "\n***** Leyendo el MBR *****\n"
    mbr = MBR()
    res, msg = Fread_displacement(file, 0, mbr)
    if not res:
        result += msg + f'No se pudo leer el MBR del disco {path}\n'
        file.close()
        return result
    result += mbr.display_info()
    
    result += "\n***** Buscando la particion *****\n"
    partition = mbr.get_partitionbyName(name, file)
    if not partition:
        result += f'No se encontro la particion {name} en el disco {path}\n'
        file.close()
        return result
    
    if not isinstance(partition, EBR):
        if partition.part_type.decode() == 'e':
            result += f'No se puede montar una particion extendida\n'
            file.close()
            return result

    if partition.part_status.decode() == 'y':
        result += f'La particion {name} ya esta montada\n'
        file.close()
        return result
    
    result += partition.display_info()
    # We make the id of the partition
    result += '\n***** Creando ID de la particion *****\n'
    _, disk_name = os.path.split(path)
    disk_name = disk_name[:-4]

    index = 1
    for data in mounted_partitions:
        if data['path'] == path:
            index = int(data['id'][2:3]) + 1

    id = '94' + str(index) + disk_name
    result += f'ID: {id}\n'

    # We add the partition to the list
    result += '\n***** Montando la partición *****\n'
    partition.part_status = b'y'
    if not mbr.set_partitionbyName(name, partition, file):
        result += f'No se pudo montar la particion {name} del disco {path}\n'
        file.close()
        return result
    
    res, msg = Fwrite_displacement(file, 0, mbr)
    if not res:
        result += msg + f'No se pudo escribir el MBR del disco {path}\n'
        file.close()
        return result
    
    mounted_partitions.append({'id': id, 'path': path, 'name': name, 'partition': partition})
    
    try:
        file.close()
    except:
        result += f'No se pudo cerrar el disco {path}\n'
        return result
    
    result += f'Particion {name} montada con exito\n'
    result += display_mounted_partitions()
    result += "\nFinalizando MOUNT\n\n"
    return result