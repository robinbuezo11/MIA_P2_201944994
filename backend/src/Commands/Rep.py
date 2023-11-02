from Objects.MBR import MBR
from Utils.Fmanager import *
from Utils.Utilities import *
from Utils.Globals import *

def rep(name, path, id, ruta):
    result = 'Ejecutando el comando REP\n'
    result += '***** Buscando el disco *****\n'
    mounted_partition = get_mounted_partitionbyId(id)
    if not mounted_partition:
        result += f'No se encontró la partición {id}\n'
        return result
    
    result += '***** Abriendo el disco *****\n'
    try:
        file = open(mounted_partition['path'], 'rb+')
    except:
        result += f'No se pudo abrir el disco {mounted_partition["path"]}\n'
        return result
    
    result += '***** Leyendo el MBR *****\n'
    mbr = MBR()
    mbr, msg = Fread_displacement(file, 0, mbr)
    if not mbr:
        result += f'No se pudo leer el MBR del disco {mounted_partition["path"]}\n'
        file.close()
        return result + msg
    
    partition = mounted_partition['partition']
    
    # We have to check the type of report to generate in base of the name
    result += '***** Generando el reporte *****\n'
    if name == 'mbr':
        res, code = mbr.generate_report_mbr(file)
        if not res:
            result += code
            file.close()
            return result

        if not execute_graphviz(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'
    
    elif name == 'disk':
        res, code = mbr.generate_report_disk(file, id[3:])
        if not res:
            result += code
            file.close()
            return result

        if not execute_graphviz(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'

    # elif name == 'inode':
    #     code = partition.generate_report_inode(file)

    #     if not execute_graphviz(code, path):
    #         printError(f'No se pudo generar el reporte {name}')
    #         file.close()
    #         return False
    #     printSuccess(f'Se genero el reporte {name} correctamente')

    # elif name == 'block':
    #     code = partition.generate_report_block(file)

    #     if not execute_graphviz(code, path):
    #         printError(f'No se pudo generar el reporte {name}')
    #         file.close()
    #         return False
    #     printSuccess(f'Se genero el reporte {name} correctamente')

    elif name == 'bm_inode':
        res, code = partition.generate_report_bm_inode(file)
        if not res:
            result += code
            file.close()
            return result

        if not save_txt20(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'

    elif name == 'bm_block':
        res, code = partition.generate_report_bm_block(file)
        if not res:
            result += code
            file.close()
            return result

        if not save_txt20(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'

    elif name == 'tree':
        res, code = partition.generate_report_tree(file)
        if not res:
            result += code
            file.close()
            return result

        if not execute_graphviz(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'

    elif name == 'sb':
        res, code = partition.generate_report_sb(file)
        if not res:
            result += code
            file.close()
            return result

        if not execute_graphviz(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'
        
    elif name == 'file':
        res, code = partition.generate_report_file(file, ruta)
        if not res:
            result += code
            file.close()
            return result

        if not save_txt(code, path):
            result += f'No se pudo generar el reporte {name}\n'
            file.close()
            return result
        result += f'Se genero el reporte {name} correctamente\n'

    # elif name == 'ls':
    #     code = partition.generate_report_ls(file, ruta)

    #     if not execute_graphviz(code, path):
    #         printError(f'No se pudo generar el reporte {name}')
    #         file.close()
    #         return False
    #     printSuccess(f'Se genero el reporte {name} correctamente')

    # elif name == 'journaling':
    #     code = partition.generate_report_journaling(file)

    #     if not execute_graphviz(code, path):
    #         printError(f'No se pudo generar el reporte {name}')
    #         file.close()
    #         return False
    #     printSuccess(f'Se genero el reporte {name} correctamente')
        
    try:
        file.close()
    except:
        result += f'No se pudo cerrar el disco {mounted_partition["path"]}\n'
        return result
    
    result += '***** Finalizando REP *****\n'
    return result

def execute_graphviz(code, path):
    if code != '':
        try:
            dir, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            if dir != '':
                if not os.path.exists(dir):
                    os.makedirs(dir)
            dot = open(dir + '/' + name + '.dot', 'w+')
            dot.write(code)
            dot.close()
            os.system(f'dot -T{ext[1:]} {dir}/{name}.dot -o {dir}/{name}.{ext[1:]}')
        except Exception as e:
            printError(f'{e}')
            return False
    return True

def save_txt20(code, path):
    if code != '':
        try:
            dir, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            if dir != '':
                if not os.path.exists(dir):
                    os.makedirs(dir)
            txt = open(dir + '/' + name + '.txt', 'w+')
            lines = [code[i:i+20] for i in range(0, len(code), 20)]
            txt.write('\n'.join(lines))
            txt.close()
        except Exception as e:
            printError(f'{e}')
            return False
    return True

def save_txt(code, path):
    if code != '':
        try:
            dir, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            if dir != '':
                if not os.path.exists(dir):
                    os.makedirs(dir)
            txt = open(dir + '/' + name + '.txt', 'w+')
            txt.write(code)
            txt.close()
        except Exception as e:
            printError(f'{e}')
            return False
    return True
