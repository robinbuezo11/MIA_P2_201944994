from Utils.Globals import *
from Utils.NodesManager import *
from Objects.SuperBlock import *

def login(user, password, id_partition):
    if len(user_session) > 0:
        return False, f'Ya hay una sesión iniciada\n'
    
    if not id_partition or not user or not password:
        return False, f'Faltan parámetros\n'
    
    partition = get_mounted_partitionbyId(id_partition)
    if not partition:
        return False, f'No se encontró la partición\n'
    
    superblock = SuperBlock()
    file = open(partition['path'], 'rb+')

    superblock, msg = Fread_displacement(file, partition['partition'].part_start, superblock)
    if not superblock:
        return False, msg

    indexInode, msg = initSearch(f'/users.txt', file, superblock)
    if indexInode == -1:
        return False, msg

    inodeFile = Inode()
    inodeFile, msg = Fread_displacement(file, superblock.s_inode_start + indexInode * superblock.s_inode_s, inodeFile)
    if not inodeFile:
        return False, msg

    fileData = getInodeFileData(inodeFile, file, superblock)
    splitFileData = fileData.split('\n')
    splitFileData.pop()

    for line in splitFileData:
        splitLine = line.split(',')
        if splitLine[1] == 'U':
            if splitLine[3] == user and splitLine[4] == password:
                user_session.append(user)
                return True, f'Se inició sesión correctamente\n'
            
    return False, f'No se encontró el usuario\n'