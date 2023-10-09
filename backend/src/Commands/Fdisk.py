import struct
import copy
from Utils.Fmanager import *
from Objects.Partition import Partition
from Objects.MBR import MBR
from Objects.EBR import EBR

def fdisk(path, size, unit, name, type, fit, delete, add):
    printConsole('Ejecutando el comando FDISK')
    print("***** Abriendo Disco *****")
    try:
        file = open(path, "rb+")
    except Exception as e:
        printError(f"Error al abrir el disco: {e}")
        return False
    
    print("\n***** Leyendo MBR *****")
    mbr = MBR()
    mbr = Fread_displacement(file, 0, mbr)
    if not mbr:
        printError("No se pudo leer el MBR")
        file.close()
        return False
    
    mbr.display_info()

    # Here we have to check wich operation we are going to do
    
    # *************************************** DELETE ***************************************
    # ****************************************************************************************
    if delete:
        if not printWarning(f"¿Seguro que desea eliminar la partición {name.upper()}? (s/n)"):
            printConsole("Cancelando FDISK\n")
            file.close()
            return False
        
        print("\n***** Eliminando PARTICIÓN *****")
        try:
            found = False
            for i, partition in enumerate(mbr.partitions):
                if partition.part_name.decode() == name:
                    partition.display_info()
                    # Here we have to delete the partition from the disk
                    if Fwrite_displacement_data(file, partition.part_start, b'\0'*partition.part_s):
                        printSuccess("Se elimino la partición del disco correctamente")
                    else:
                        printError("No se pudo eliminar la partición del disco")
                        file.close()
                        return False
                    # Here we delete the partition from the MBR
                    mbr.partitions[i] = Partition()
                    printSuccess("Se elimino la partición del MBR correctamente")
                    found = True
                    break

            if not found:
                printError(f"No se encontro la partición {name}")
                file.close()
                return False
            
            print("\n***** Escribiendo MBR *****")
            if not write_mbr(file, mbr):
                file.close()
                return False

        except Exception as e:
            printError(f"{e}")
            file.close()
            return False
        printSuccess("Se elimino la partición correctamente\n")
        
    # *************************************** ADD ***************************************
    # ************************************************************************************
    elif add:
        size_bytes = get_sizeB(add, unit)
        # Comprobate if the partition exists and if this have space at the end
        print("\n***** Buscando PARTICION *****")
        found_partition = None
        position = -1
        for i, partition in enumerate(mbr.partitions):
            if partition.part_name.decode() == name:
                found_partition = partition
                position = i
                break

        if not found_partition:
            printError(f"No se encontro la partición {name}")
            file.close()
            return False

        setted = False
        # In case that the partition is the last one and the size is positive
        if position == 3 and size_bytes > 0:
            if (found_partition.part_start + found_partition.part_s) + size_bytes > mbr.mbr_tamano:
                printError("No hay espacio suficiente en el disco")
                file.close()
                return False
            else:
                found_partition.part_s += size_bytes
                printSuccess(f"Se agregaron {size_bytes}B a la partición {name.upper()}")
                found_partition.display_info()
                setted = True
                
        # In case that the partition is not the last one and the size is positive
        elif position < 3 and size_bytes > 0:
            index = position + 1
            nextStart = mbr.mbr_tamano
            while index < 4:
                if mbr.partitions[index].part_s != -1:
                    nextStart = mbr.partitions[index].part_start
                    break
                index += 1
            if (found_partition.part_start + found_partition.part_s) + size_bytes > nextStart:
                printError("No hay espacio suficiente en el disco")
                file.close()
                return False
            else:
                found_partition.part_s += size_bytes
                printSuccess(f"Se agregaron {size_bytes}B a la partición {name.upper()}")
                found_partition.display_info()
                setted = True

        # In case that the partition's size is negative
        elif size_bytes < 0:
            if found_partition.part_s + size_bytes <= 0:
                printError("La partición no puede tener un tamaño negativo o cero")
                file.close()
                return False
            else:
                new_size = found_partition.part_s + size_bytes
                if Fwrite_displacement_data(file, found_partition.part_start + new_size, b'\0'*abs(size_bytes)):
                    found_partition.part_s += size_bytes
                    printSuccess(f"Se redujeron {abs(size_bytes)}B a la partición {name.upper()}")
                    found_partition.display_info()
                    setted = True
                else:
                    printError("No se pudo eliminar espacio a la partición")
                    file.close()
                    return False
                            
        if setted:
            print("\n***** Escribiendo MBR *****")
            mbr.partitions[position] = found_partition
            if not write_mbr(file, mbr):
                file.close()
                return False
            printSuccess("Se modifico la partición correctamente\n")
                
    # *************************************** CREATE ***************************************
    # ****************************************************************************************
    else:
        # Validations of the name and type of the partition
        print("\n***** Buscando Espacio *****")
        extended_partition = None
        for i, partition in enumerate(mbr.partitions):
            if partition.part_name.decode() == name:
                printError(f"Ya existe una partición con el nombre {name.upper()}")
                file.close()
                return False
            if partition.part_type.decode() == 'e':
                extended_partition = partition

        if type == 'e' and extended_partition:
            printError("Ya existe una partición extendida")
            file.close()
            return False
        
        if type == 'l' and not extended_partition:
            printError("No existe una partición extendida para crear una lógica")
            file.close()
            return False
        
        # Here we create a new partition
        size_bytes = get_sizeB(size, unit)

        if type in ['p', 'e']:
            start = len(mbr.doSerialize())
            foundSpace = False
            partition_index = 0
                
            for i, partition in enumerate(mbr.partitions):
                print(f"Particion {i+1}:")
                if partition.part_s != -1:
                    start = partition.part_start + partition.part_s
                    print("Ocupada")
                else:
                    # Here we have to check if the space is enough
                    indx = i + 1
                    nextStart = mbr.mbr_tamano
                    while indx < 4:
                        if mbr.partitions[indx].part_s != -1:
                            nextStart = mbr.partitions[indx].part_start
                            break
                        indx += 1
                    if start + size_bytes <= nextStart:
                        foundSpace = True
                        partition_index = i
                        break
                    else:
                        print("No hay espacio")

            if not foundSpace:
                printError("No hay espacio disponible")
                file.close()
                return False

            print("\n***** Creando PARTICIÓN *****")
            part = Partition()
            part.set_info('n',type,fit,start,size_bytes,name)
            part.display_info()

            print("\n***** Escribiendo PARTICIÓN *****")
            mbr.partitions[partition_index] = part
            if type == 'e':
                # If the partition is extended we have to create the EBR inside
                print("\n***** Creando EBR *****")
                ebr = EBR()
                ebr.set_info('n', (b'\0').decode(), start + struct.calcsize(EBR().get_const()), -1, -1, (b'\0'*16).decode())
                if struct.calcsize(ebr.get_const()) > size_bytes:
                    printError("El tamaño de la partición es muy pequeño para el EBR")
                    file.close()
                    return False
                if not Fwrite_displacement(file, start, ebr):
                    printError("No se pudo crear el EBR")
                    file.close()
                    return False
                else:
                    printSuccess("Se creo el EBR correctamente")
            if not write_mbr(file, mbr):
                file.close()
                return False
            printSuccess("Se creo la partición correctamente\n")
        else:
            # Here we have to create a logical partition
            ebr = EBR()
            print("\n***** Leyendo EBR *****")
            ebr = Fread_displacement(file, extended_partition.part_start, ebr)
            if not ebr:
                printError("No se pudo leer el EBR")
                file.close()
                return False
            # Validations of the name
            ebraux = copy.deepcopy(ebr)
            while ebraux.part_next != -1:
                if ebraux.part_name.decode() == name:
                    printError(f"Ya existe una partición con el nombre {name.upper()}")
                    file.close()
                    return False
                ebraux = Fread_displacement(file, ebraux.part_next, ebraux)
                if not ebraux:
                    printError("No se pudo leer el EBR")
                    file.close()
                    return False
            if ebraux.part_name.decode() == name:
                printError(f"Ya existe una partición con el nombre {name.upper()}")
                file.close()
                return False
            
            # Here we have to search a space to create the partition
            foundSpace = False
            ebrsize = struct.calcsize(EBR().get_const())
            ebraux = copy.deepcopy(ebr)
            while ebraux.part_next != -1:
                if ebraux.part_next - (ebraux.part_start + ebraux.part_s) >= ebrsize + size_bytes:
                    ebr.set_info('n', fit, ebraux.part_start + ebraux.part_s + ebrsize, size_bytes, ebraux.part_next, name)
                    ebraux.part_next = ebr.part_start - ebrsize
                    foundSpace = True
                    break
                ebraux = Fread_displacement(file, ebraux.part_next, ebraux)
                if not ebraux:
                    printError("No se pudo leer el EBR")
                    file.close()
                    return False
                
            isFirst = False
            if not foundSpace:
                # If is the first and is empty
                if ebraux.part_s == -1:
                    if ebraux.part_start + size_bytes <= extended_partition.part_start + extended_partition.part_s:
                        isFirst = True
                        ebr.set_info('n', fit, ebraux.part_start, size_bytes, -1, name)
                        foundSpace = True
                    else:
                        printError("No hay espacio disponible")
                        file.close()
                        return False
                else:
                    if ebraux.part_start + ebraux.part_s + ebrsize + size_bytes <= extended_partition.part_start + extended_partition.part_s:
                        ebr.set_info('n', fit, ebraux.part_start + ebraux.part_s + ebrsize, size_bytes, -1, name)
                        ebraux.part_next = ebr.part_start - ebrsize
                        foundSpace = True
                    else:
                        printError("No hay espacio disponible")
                        file.close()
                        return False
            
            print("\n***** Creando PARTICIÓN *****")
            ebr.display_info()
            print("\n***** Escribiendo EBR *****")
            if isFirst:
                # If is the first we have to write the EBR in the extended partition
                if not Fwrite_displacement(file, extended_partition.part_start, ebr):
                    printError("No se pudo escribir el EBR")
                    file.close()
                    return False
                else:
                    printSuccess("Se creo el EBR correctamente")
            else:
                # If is not the first we have to write the EBR previous with the updated next and the new EBR
                if not Fwrite_displacement(file, ebraux.part_start - ebrsize, ebraux):
                    printError("No se pudo escribir el EBR")
                    file.close()
                    return False
                
                if not Fwrite_displacement(file, ebr.part_start - ebrsize, ebr):
                    printError("No se pudo escribir el EBR")
                    file.close()
                    return False
            printSuccess("Se creo la partición correctamente\n")

    file.close()
    printConsole("Finalizando FDISK\n")
    return True

def write_mbr(file, mbr):
    if Fwrite_displacement(file, 0, mbr):
        printSuccess("Se escribio el MBR correctamente")
        return True
    else:
        printError("No se pudo escribir el MBR")
        return False