from Utils.load import *
from Objects.Inode import *
from Objects.FolderBlock import *
from Objects.FileBlock import *

def initSearch(path,file,superblock):
    StepsPath = path.split("/")
    StepsPath.pop(0)
    
    if(len(StepsPath)==0):
        return 0
    
    Inode0 = Inode()
    Fread_displacement(file, superblock.s_inode_start, Inode0)
    return SarchInodeByPath(StepsPath,Inode0,file,superblock)

def SarchInodeByPath(StepsPath,Inode,file,superblock):
    SearchedName = StepsPath.pop(0)
       
    for i in Inode.i_block:
        if(i != -1):
            #DIRECTS
            folderblock = FolderBlock()
            folderblock, msg = Fread_displacement(file, superblock.s_block_start + i * superblock.s_block_s, folderblock)
            if not folderblock:
                return -1, msg

            for content in folderblock.b_content:
                if(content.b_inodo != -1):
                    if(content.b_name.decode() == SearchedName):
                        if(len(StepsPath)==0):
                            return content.b_inodo, ''
                        else:
                            nextinode = Inode()
                            nextinode, msg = Fread_displacement(file, superblock.s_inode_start + content.b_inodo * superblock.s_inode_s, nextinode)
                            if not nextinode:
                                return -1, msg
                            return SarchInodeByPath(StepsPath,nextinode,file)

            # else:
                # #INDIRECTS
                # pass  


    
def getInodeFileData(inode,file,superblock):
    content = ""
    for i in inode.i_block:
        if(i != -1):
            #DIRECTS
            fileblock = FileBlock()
            fileblock, msg = Fread_displacement(file, superblock.s_block_start + i * superblock.s_block_s, fileblock)
            if not fileblock:
                return -1, msg

            content += fileblock.b_content.decode()
    
            # else:
            #     #INDIRECTS
            #     pass  

    return content
