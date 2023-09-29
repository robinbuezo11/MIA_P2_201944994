import struct
import math
from datetime import datetime
from Utils.Utilities import *
from Utils.Globals import *
from Utils.Fmanager import *
from Objects.SuperBlock import SuperBlock
from Objects.Inode import Inode
from Objects.FileBlock import FileBlock
from Objects.Journaling import Journaling
from Objects.FolderBlock import FolderBlock

def mkfs(id, fs):
    printConsole('Ejecutando el comando MKFS')
    print("***** Buscando Particion *****")
    mounted_partition = get_mounted_partitionbyId(id)
    if not mounted_partition:
        printError(f'No se encontró la partición {id}')
        return False
    
    partition = mounted_partition['partition']
    path = mounted_partition['path']
    numerator = partition.part_s - struct.calcsize(SuperBlock().get_const())
    denominator = 4 + struct.calcsize(Inode().get_const()) + 3 * struct.calcsize(FileBlock().get_const())
    if fs == '3fs':
        denominator += Journaling().get_const_num()
    n = math.floor(numerator / denominator)

    superblock = SuperBlock()
    superblock.s_inodes_count = n
    superblock.s_blocks_count = 3 * n
    superblock.s_free_inodes_count = n
    superblock.s_free_blocks_count = 3 * n

    date = coding_str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 19)
    superblock.s_mtime = date
    superblock.s_umtime = date
    superblock.s_mnt_count = 1

    
    print("***** Formateando Particion *****")
    if fs == '2fs':
        if not format_2fs(n, partition, path, superblock, date):
            printError(f'No se pudo formatear la particion {partition.part_name}')
            return False
    else:
        if not format_3fs(n, partition, path, superblock, date):
            printError(f'No se pudo formatear la particion {partition.part_name}')
            return False
        
    printSuccess(f'Se formateo la particion {partition.part_name} con {fs}')
    print("***** Finalizando MKFS *****\n")

def format_2fs(n, partition, path, superblock, date):
    # Without Journaling
    superblock.s_filesystem_type = 2
    superblock.s_bm_inode_start = partition.part_start + struct.calcsize(SuperBlock().get_const())
    superblock.s_bm_block_start = superblock.s_bm_inode_start + n
    superblock.s_inode_start = superblock.s_bm_block_start + 3 * n
    superblock.s_block_start = superblock.s_inode_start + n * struct.calcsize(Inode().get_const())
    superblock.s_inode_s = struct.calcsize(Inode().get_const())
    superblock.s_block_s = struct.calcsize(FileBlock().get_const())

    superblock.s_free_inodes_count -= 2
    superblock.s_free_blocks_count -= 2

    superblock.s_first_ino = 2
    superblock.s_first_blo = 2

    # Create Root Folder
    inode0 = Inode()
    inode0.i_uid = 1
    inode0.i_gid = 1
    inode0.i_s = 0
    inode0.i_atime = date
    inode0.i_ctime = date
    inode0.i_mtime = date
    inode0.i_type = b'0'
    inode0.i_perm = 664
    inode0.i_block[0] = 0

    folderblock = FolderBlock()
    folderblock.b_content[0].setInfo(0, '.')
    folderblock.b_content[1].setInfo(0, '..')
    folderblock.b_content[2].setInfo(1, 'users.txt')

    # Create User File
    inode1 = Inode()
    inode1.i_uid = 1
    inode1.i_gid = 1
    inode1.i_s = struct.calcsize(FileBlock().get_const())
    inode1.i_atime = date
    inode1.i_ctime = date
    inode1.i_mtime = date
    inode1.i_type = b'1'
    inode1.i_perm = 664
    inode1.i_block[0] = 1

    data_user = '1,G,root\n1,U,root,root,123\n'
    fileblock = FileBlock()
    fileblock.b_content = coding_str(data_user, 64)

    # Write SuperBlock
    try:
        file = open(path, 'rb+')
    except:
        printError(f'No se pudo abrir el disco {path}')
        return False
    
    if not Fwrite_displacement(file, partition.part_start, superblock):
        printError(f'No se pudo escribir el SuperBloque en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Super Bloque en el disco {path}')

    # Write Bitmap Inode
    bitmap = b'1' * 2 + b'0' * (n - 2)
    if not Fwrite_displacement_data(file, superblock.s_bm_inode_start, bitmap):
        printError(f'No se pudo escribir el Bitmap de Inodos en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Bitmap de Inodos en el disco {path}')
    
    # Write Bitmap Block
    bitmap = b'1' * 2 + b'0' * (3 * n - 2)
    if not Fwrite_displacement_data(file, superblock.s_bm_block_start, bitmap):
        printError(f'No se pudo escribir el Bitmap de Bloques en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Bitmap de Bloques en el disco {path}')
    
    # Write Inode Table
    inode = Inode()
    for i in range(2, n):
        if not Fwrite_displacement(file, superblock.s_inode_start + i * struct.calcsize(Inode().get_const()), inode):
            printError(f'No se pudo escribir el Inodo {i} en el disco {path}')
            file.close()
            return False
    printSuccess(f'Se escribió la Tabla de Inodos en el disco {path}')

    # Write Block Table
    block = FileBlock()
    for i in range(2, 3 * n):
        if not Fwrite_displacement(file, superblock.s_block_start + i * struct.calcsize(FileBlock().get_const()), block):
            printError(f'No se pudo escribir el Bloque {i} en el disco {path}')
            file.close()
            return False
    printSuccess(f'Se escribió la Tabla de Bloques en el disco {path}')
        
    # Write Root Folder
    if not Fwrite_displacement(file, superblock.s_inode_start, inode0):
        printError(f'No se pudo escribir el Inodo 0 en el disco {path}')
        file.close()
        return False
    if not Fwrite_displacement(file, superblock.s_block_start, folderblock):
        printError(f'No se pudo escribir el Bloque 0 en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió la Carpeta Raiz en el disco {path}')
    
    # Write User File
    if not Fwrite_displacement(file, superblock.s_inode_start + struct.calcsize(Inode().get_const()), inode1):
        printError(f'No se pudo escribir el Inodo 1 en el disco {path}')
        file.close()
        return False
    if not Fwrite_displacement(file, superblock.s_block_start + struct.calcsize(FileBlock().get_const()), fileblock):
        printError(f'No se pudo escribir el Bloque 1 en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Archivo de Usuarios en el disco {path}')
    
    try:
        file.close()
    except:
        printError(f'No se pudo cerrar el disco {path}')
        return False

    return True

def format_3fs(n, partition, path, superblock, date):
    # With Journaling
    superblock.s_filesystem_type = 3
    superblock.s_bm_inode_start = partition.part_start + struct.calcsize(SuperBlock().get_const()) + Journaling().get_const_num()
    superblock.s_bm_block_start = superblock.s_bm_inode_start + n
    superblock.s_inode_start = superblock.s_bm_block_start + 3 * n
    superblock.s_block_start = superblock.s_inode_start + n * struct.calcsize(Inode().get_const())
    superblock.s_inode_s = struct.calcsize(Inode().get_const())
    superblock.s_block_s = struct.calcsize(FileBlock().get_const())

    superblock.s_free_inodes_count -= 2
    superblock.s_free_blocks_count -= 2

    superblock.s_first_ino = 2
    superblock.s_first_blo = 2

    journaling = Journaling()

    # Create Root Folder
    inode0 = Inode()
    inode0.i_uid = 1
    inode0.i_gid = 1
    inode0.i_s = 0
    inode0.i_atime = date
    inode0.i_ctime = date
    inode0.i_mtime = date
    inode0.i_type = b'0'
    inode0.i_perm = 664
    inode0.i_block[0] = 0

    folderblock = FolderBlock()
    folderblock.b_content[0].setInfo(0, '.')
    folderblock.b_content[1].setInfo(0, '..')
    folderblock.b_content[2].setInfo(1, 'users.txt')

    journaling.j_journals[0].set_info(0, '/', '-', date.decode())

    # Create User File
    inode1 = Inode()
    inode1.i_uid = 1
    inode1.i_gid = 1
    inode1.i_s = struct.calcsize(FileBlock().get_const())
    inode1.i_atime = date
    inode1.i_ctime = date
    inode1.i_mtime = date
    inode1.i_type = b'1'
    inode1.i_perm = 664
    inode1.i_block[0] = 1

    data_user = '1,G,root\n1,U,root,root,123\n'
    fileblock = FileBlock()
    fileblock.b_content = coding_str(data_user, 64)

    journaling.j_journals[1].set_info(1, 'users.txt', data_user, date.decode())

    # Write SuperBlock
    try:
        file = open(path, 'rb+')
    except:
        printError(f'No se pudo abrir el disco {path}')
        return False
    
    if not Fwrite_displacement(file, partition.part_start, superblock):
        printError(f'No se pudo escribir el SuperBloque en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Super Bloque en el disco {path}')

    # Write Journaling
    if not Fwrite_displacement(file, partition.part_start + struct.calcsize(SuperBlock().get_const()), journaling):
        printError(f'No se pudo escribir el Journaling en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Journaling en el disco {path}')

    # Write Bitmap Inode
    bitmap = b'1' * 2 + b'0' * (n - 2)
    if not Fwrite_displacement_data(file, superblock.s_bm_inode_start, bitmap):
        printError(f'No se pudo escribir el Bitmap de Inodos en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Bitmap de Inodos en el disco {path}')
    
    # Write Bitmap Block
    bitmap = b'1' * 2 + b'0' * (3 * n - 2)
    if not Fwrite_displacement_data(file, superblock.s_bm_block_start, bitmap):
        printError(f'No se pudo escribir el Bitmap de Bloques en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Bitmap de Bloques en el disco {path}')
    
    # Write Inode Table
    inode = Inode()
    for i in range(2, n):
        if not Fwrite_displacement(file, superblock.s_inode_start + i * struct.calcsize(Inode().get_const()), inode):
            printError(f'No se pudo escribir el Inodo {i} en el disco {path}')
            file.close()
            return False
    printSuccess(f'Se escribió la Tabla de Inodos en el disco {path}')

    # Write Block Table
    block = FileBlock()
    for i in range(2, 3 * n):
        if not Fwrite_displacement(file, superblock.s_block_start + i * struct.calcsize(FileBlock().get_const()), block):
            printError(f'No se pudo escribir el Bloque {i} en el disco {path}')
            file.close()
            return False
    printSuccess(f'Se escribió la Tabla de Bloques en el disco {path}')
        
    # Write Root Folder
    if not Fwrite_displacement(file, superblock.s_inode_start, inode0):
        printError(f'No se pudo escribir el Inodo 0 en el disco {path}')
        file.close()
        return False
    if not Fwrite_displacement(file, superblock.s_block_start, folderblock):
        printError(f'No se pudo escribir el Bloque 0 en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió la Carpeta Raiz en el disco {path}')
    
    # Write User File
    if not Fwrite_displacement(file, superblock.s_inode_start + struct.calcsize(Inode().get_const()), inode1):
        printError(f'No se pudo escribir el Inodo 1 en el disco {path}')
        file.close()
        return False
    if not Fwrite_displacement(file, superblock.s_block_start + struct.calcsize(FileBlock().get_const()), fileblock):
        printError(f'No se pudo escribir el Bloque 1 en el disco {path}')
        file.close()
        return False
    printSuccess(f'Se escribió el Archivo de Usuarios en el disco {path}')
    
    try:
        file.close()
    except:
        printError(f'No se pudo cerrar el disco {path}')
        return False

    return True