import ply.yacc as yacc
# Import all from lexer
from lexer import *
from Commands.Mkdisk import *
from Commands.Rmdisk import *
from Commands.Fdisk import *
from Commands.Execute import *
from Commands.Rep import *
from Commands.Mount import *
from Commands.Unmount import *
from Commands.Pause import *
from Commands.Mkfs import *

# Grammar rules
def p_init(t):
    'init : list_commands'
    t[0] = t[1]
    return t[0]

def p_list_commands(t):
    '''list_commands : list_commands commands
                    | commands'''
    if len(t) != 2:
        t[1] += t[2]
        t[0] = t[1]
    else:
        t[0] = t[1]
    
def p_commands(t): 
    '''commands : command_mkdisk
                | command_rmdisk
                | command_fdisk
                | command_mount
                | command_mkfs

                | command_pause
                | command_rep
                | COMMENT'''
    t[0] = t[1]

#------------------------------------------------------------
#------------------------ EXECUTE ---------------------------
# def p_command_execute(t):
#     '''command_execute : EXECUTE GUION PATH IGUAL CADENA
#                        | EXECUTE GUION PATH IGUAL CADENA_SC'''
#     data = execute(t[5])
#     if data:
#         commands = data.split('\n')
#         line = 1
#         for command in commands:
#             print(f'Linea {line}: {command}\n')
#             line += 1
#             if command == '' or command[0] == '#':
#                 continue
#             parser.parse(command)

#------------------------------------------------------------
#------------------------ MKDISK ----------------------------
def p_command_mkdisk(t):                                       
    'command_mkdisk : MKDISK params_mkdisk'

    required_params = ['path', 'size']

    t[0] = ''    
    for param in required_params:
        if param not in t[2]:
            t[0] = f'MKDISK -> Parametro {param} requerido\n'
            return t[0]
        
    path = t[2].get('path')
    size = t[2].get('size')
    unit = t[2].get('unit', 'm')
    fit = t[2].get('fit', 'ff')

    if path[-3:] != 'dsk':
        t[0] += f'MKDISK -> La extension del archivo {path} debe ser .dsk\n'
        return t[0]

    if unit not in ['m', 'k']:
        try:
            return t[0] + f'MKDISK -> Unidad {str(unit).upper()} no reconocida\n'
        except:
            return t[0] + f'MKDISK -> Unidad {unit} no reconocida\n'
    
    if size < 0:
        return t[0] + f'MKDISK -> Tamaño {size} no valido\n'
    
    if fit not in ['bf', 'ff', 'wf']:
        try:
            return t[0] + f'MKDISK -> Ajuste {str(fit).upper()} no reconocido\n'
        except:
            return t[0] + f'MKDISK -> Ajuste {fit} no reconocido\n'
    
    t[0] += mkdisk(path, size, unit, fit)

def p_params_mkdisk(t):
    '''params_mkdisk : params_mkdisk param_mkdisk
                    | param_mkdisk'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_param_mkdisk(t):
    '''param_mkdisk : GUION PATH IGUAL CADENA
                    | GUION PATH IGUAL CADENA_SC
                    | GUION SIZE IGUAL ENTERO
                    | GUION UNIT IGUAL CADENA_SC
                    | GUION FIT IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ RMDISK ----------------------------
def p_command_rmdisk(t):
    '''command_rmdisk : RMDISK GUION PATH IGUAL CADENA
                      | RMDISK GUION PATH IGUAL CADENA_SC'''
    
    t[0] = ''
    if t[5][-3:] != 'dsk':
        t[0] += f'RMDISK -> La extension del archivo {t[5]} debe ser .dsk\n'
        return

    t[0] += rmdisk(t[5])

#------------------------------------------------------------
#------------------------ FDISK -----------------------------
def p_command_fdisk(t):
    'command_fdisk : FDISK params_fdisk'
    
    t[0] = ''
    required_params = ['path', 'name']

    # Check if exists more than one operation
    # op_params = ['delete', 'add']
    # op_count = 0
    # for param in op_params:
    #     if param in t[2]:
    #         op_count += 1
    # if op_count > 1:
    #     t[0] += f'FDISK -> No se puede usar mas de un parametro entre {op_params}\n'
    #     return
    
    # Search the first operation if exists
    # op = None
    # for param in t[2]:
    #     if param == 'delete':
    #         op = 'delete'
    #         break
    #     elif param == 'add':
    #         op = 'add'
    #         break

    # if not exists operation, add size how required param
    # if not op:
    required_params.append('size')

    for param in required_params:
        if param not in t[2]:
            t[0] += f'FDISK -> Parametro {param} requerido\n'
            return
        
    path = t[2].get('path')
    size = t[2].get('size', 0)
    unit = t[2].get('unit', 'k')
    name = t[2].get('name')
    type = t[2].get('type', 'p')
    fit = t[2].get('fit', 'wf')
    # delete = t[2].get('delete', 'full')
    # add = t[2].get('add', 0)

    if unit not in ['b', 'k', 'm']:
        try:
            t[0] += f'FDISK -> Unidad {str(unit).upper()} no reconocida\n'
        except:
            t[0] += f'FDISK -> Unidad {unit} no reconocida\n'
        return
    
    if size < 0:
        t[0] += f'FDISK -> Tamaño {size} no valido\n'
        return
    
    if type not in ['p', 'e', 'l']:
        try:
            t[0] += f'FDISK -> Tipo {str(type).upper()} no reconocido\n'
        except:
            t[0] += f'FDISK -> Tipo {type} no reconocido\n'
        return
    
    if fit not in ['bf', 'ff', 'wf']:
        try:
            t[0] += f'FDISK -> Ajuste {str(fit).upper()} no reconocido\n'
        except:
            t[0] += f'FDISK -> Ajuste {fit} no reconocido\n'
        return
    
    # if delete != 'full':
    #     try:
    #         printError(f'FDISK -> Eliminacion {str(delete).upper()} no reconocida')
    #     except:
    #         printError(f'FDISK -> Eliminacion {delete} no reconocida')
    #     return
    
    # if op == 'delete':
    #     add = None
    # elif op == 'add':
    #     if add == 0:
    #         printError(f'FDISK -> No se puede agregar 0')
    #     delete = None
    # else:
    #     delete = None
    #     add = None
    
    t[0] += fdisk(path, size, unit, name, type, fit)

def p_params_fdisk(t):
    '''params_fdisk : params_fdisk param_fdisk
                    | param_fdisk'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_param_fdisk(t):
    '''param_fdisk : GUION PATH IGUAL CADENA
                    | GUION PATH IGUAL CADENA_SC
                    | GUION SIZE IGUAL ENTERO
                    | GUION UNIT IGUAL CADENA_SC
                    | GUION NAME IGUAL CADENA
                    | GUION NAME IGUAL CADENA_SC
                    | GUION TYPE IGUAL CADENA_SC
                    | GUION FIT IGUAL CADENA_SC'''
                    # | GUION DELETE IGUAL CADENA_SC
                    # | GUION ADD IGUAL ENTERO'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ MOUNT -----------------------------
def p_command_mount(t):
    'command_mount : MOUNT params_mount'
    
    t[0] = ''
    required_params = ['path', 'name']

    for param in required_params:
        if param not in t[2]:
            t[0] += f'MOUNT -> Parametro {param} requerido\n'
            return
        
    path = t[2].get('path')
    name = t[2].get('name')

    if path[-3:] != 'dsk':
        t[0] += f'MOUNT -> La extension del archivo {path} debe ser .dsk\n'
        return
    
    t[0] += mount(path, name)

def p_params_mount(t):
    '''params_mount : params_mount param_mount
                    | param_mount'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_param_mount(t):
    '''param_mount : GUION PATH IGUAL CADENA
                    | GUION PATH IGUAL CADENA_SC
                    | GUION NAME IGUAL CADENA
                    | GUION NAME IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ UNMOUNT ---------------------------
# def p_command_unmount(t):
#     '''command_unmount : UNMOUNT GUION ID IGUAL CADENA
#                        | UNMOUNT GUION ID IGUAL CADENA_SC'''
#     unmount(t[5])

#------------------------------------------------------------
#------------------------ MKFS ------------------------------
def p_command_mkfs(t):
    '''command_mkfs : MKFS params_mkfs'''

    t[0] = ''
    required_params = ['id']

    for param in required_params:
        if param not in t[2]:
            t[0] += f'MKFS -> Parametro {param} requerido'
            return
        
    id = t[2].get('id')
    type = t[2].get('type', 'full')
    # fs = t[2].get('fs', '2fs')

    if type not in ['full']:
        try:
            t[0] += f'MKFS -> Tipo {str(type).upper()} no reconocido'
        except:
            t[0] += f'MKFS -> Tipo {type} no renocido'
        return
    
    # if fs not in ['2fs', '3fs']:
    #     try:
    #         printError(f'MKFS -> Sistema de archivos {str(fs).upper()} no reconocido')
    #     except:
    #         printError(f'MKFS -> Sistema de archivos {fs} no reconocido')
    #     return
    
    # mkfs(id, fs)
    t[0] += mkfs(id)

def p_params_mkfs(t):
    '''params_mkfs : params_mkfs param_mkfs
                    | param_mkfs'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_param_mkfs(t):
    '''param_mkfs : GUION ID IGUAL CADENA
                    | GUION ID IGUAL CADENA_SC
                    | GUION TYPE IGUAL CADENA_SC'''
                    # | GUION FS IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ PAUSE -----------------------------
def p_command_pause(t):
    'command_pause : PAUSE'
    # pause()
    t[0] = 'Ejecutando el comando PAUSE\n'

#------------------------------------------------------------
#------------------------ REP -------------------------------
def p_command_rep(t):
    '''command_rep : REP params_rep'''

    t[0] = ''
    required_params = ['name', 'path', 'id']

    name = t[2].get('name')
    path = t[2].get('path')
    id = t[2].get('id')
    ruta = t[2].get('ruta', None)

    if name in ['file', 'ls']:
        required_params.append('ruta')

    for param in required_params:
        if param not in t[2]:
            t[0] += f'REP -> Parametro {param} requerido\n'
            return

    if name not in ['mbr', 'disk', 'bm_inode', 'bm_block', 'tree', 'sb', 'file']:
        try:
            t[0] += f'REP -> Reporte {str(name).upper()} no reconocido\n'
        except:
            t[0] += f'REP -> Reporte {name} no reconocido\n'
        return
    
    if path[-3:] not in ['png', 'jpg', 'pdf', 'txt']:
        t[0] += f'REP -> La extension del archivo {path} debe ser .txt, .png, .jpg o .pdf\n'
        return
    
    t[0] = rep(name, path, id, ruta)

def p_params_rep(t):
    '''params_rep : params_rep param_rep
                    | param_rep'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_param_rep(t):
    '''param_rep : GUION NAME IGUAL CADENA_SC
                    | GUION PATH IGUAL CADENA
                    | GUION PATH IGUAL CADENA_SC
                    | GUION ID IGUAL CADENA
                    | GUION ID IGUAL CADENA_SC
                    | GUION RUTA IGUAL CADENA
                    | GUION RUTA IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

# Error rule for syntax errors
def p_error(t):
    if t:
        # printError(f'Sintaxis no válida en la entrada: Token {t.type}, Valor {t.value}, en la linea {t.lexer.lineno}, columna {find_column(t.lexer.lexdata, t)}')
        raise Exception(f'Sintaxis no válida en la entrada: Token {t.type}, Valor {t.value}, en la linea {t.lexer.lineno}, columna {find_column(t.lexer.lexdata, t)}')
    else:
        # printError('Sintaxis no válida en la entrada')
        raise Exception('Sintaxis no válida en la entrada')

# Build the parser
parser = yacc.yacc()

def get_parser():
    return parser

# entrada = 'rmdisk -path="C:/Users/Usuario/Desktop/entrada.txt"'
# print(parser.parse(entrada))
