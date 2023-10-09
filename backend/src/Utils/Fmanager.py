import ctypes
import os
from Utils.Utilities import *

def Fwrite_displacement(file, displacement, obj):
    try:
        #print("Escribiendo en: ", displacement)
        #print("Size: ",  ctypes.sizeof(obj))
        #print("Size data: ",  len(data))
        file.seek(displacement)
        data = obj.doSerialize()
        file.write(data)
        return True
    except Exception as e:
        printError(f"{e}")
        return False
    
def Fwrite_displacement_data(file, displacement, data):
    try:
        #print("Escribiendo en: ", displacement)
        file.seek(displacement)
        file.write(data)
        return True
    except Exception as e:
        printError(f"{e}")
        return False
    
def Fread_displacement(file, displacement,obj):
    try:
        #print("Leyendo en: ", displacement)
        #print("Size: ",  ctypes.sizeof(obj))
        file.seek(displacement)
        data = file.read(len(obj.doSerialize()))
        #print("Size data: ",  len(data))
        obj.doDeserialize(data)
        return obj
    except Exception as e:
        printError(f"{e}")
        return None
    
def Fread_displacement_data(file, displacement,size):
    try:
        #print("Leyendo en: ", displacement)
        file.seek(displacement)
        data = file.read(size)
        #print("Size data: ",  len(data))
        return data
    except Exception as e:
        printError(f"{e}")
        return None

def Fcreate_file(file_name):
    try:
        fileOpen = open(file_name, "wb") 
        fileOpen.close()  
        #print("=====File created successfully!======")
        return True
    except Exception as e:
        printError(f"{e}")
        return False
    
def Fdelete_file(file_name):
    try:
        os.remove(file_name)
        return True
    except Exception as e:
        printError(f"{e}")
        return False

def Winit_size(file,size_mb):
    #mb to bytes -> mb * 1024kb/1mb * 1024b/1kb -> mb * 1024 * 1024
    buffer = b'\0'*1024
    times_to_write =  size_mb  * 1024 
    print(f"Tamaño: {len(buffer)*times_to_write} bytes")

    try:
        file.write(buffer*times_to_write)
        return True
    except Exception as e:
        printError(f"{e}")
        return False