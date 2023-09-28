from Objects.MBR import MBR
from Objects.Partition import Partition
from Utils.load import *

def rep(path):
    print('Ejecutando el comando REP')
    mrb = MBR()
    part = Partition()

    file = open(path, "rb+")

    Fread_displacement(file, 0, mrb)
    print("=====Mostrando Reporte======\n")
    mrb.display_info()
    print("****************************")
    cursor = file.tell()
    for i in range(4):
        part = Fread_displacement(file, cursor, part)
        if part:
            part.display_info()
            cursor += part.part_s * 1024
            print("****************************")
        else:
            break
    
    file.close()
    print("=====Finalizando REP======")