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

def p_list_commands(t):
    '''list_commands : list_commands commands
                    | commands'''
    
def p_commands(t): 
    '''commands : command_execute
                | command_mkdisk
                | command_rmdisk
                | command_fdisk
                | command_mount
                | command_unmount
                | command_mkfs

                | command_pause
                | command_rep
                | COMMENT'''

#------------------------------------------------------------
#------------------------ EXECUTE ---------------------------
def p_command_execute(t):
    '''command_execute : EXECUTE GUION PATH IGUAL CADENA
                       | EXECUTE GUION PATH IGUAL CADENA_SC'''
    data = execute(t[5])
    if data:
        commands = data.split('\n')
        line = 1
        for command in commands:
            print(f'Linea {line}: {command}\n')
            line += 1
            if command == '' or command[0] == '#':
                continue
            parser.parse(command)

#------------------------------------------------------------
#------------------------ MKDISK ----------------------------
def p_command_mkdisk(t):                                       
    'command_mkdisk : MKDISK params_mkdisk'

    required_params = ['path', 'size']
    
    for param in required_params:
        if param not in t[2]:
            printError(f'MKDISK -> Parametro {param} requerido')
            return
        
    path = t[2].get('path')
    size = t[2].get('size')
    unit = t[2].get('unit', 'm')
    fit = t[2].get('fit', 'ff')

    if path[-3:] != 'dsk':
        printError(f'MKDISK -> La extension del archivo {path} debe ser .dsk')
        return

    if unit not in ['m', 'k']:
        try:
            printError(f'MKDISK -> Unidad {str(unit).upper()} no reconocida')
        except:
            printError(f'MKDISK -> Unidad {unit} no reconocida')
        return
    
    if size < 0:
        printError(f'MKDISK -> Tamaño {size} no valido')
        return
    
    if fit not in ['bf', 'ff', 'wf']:
        try:
            printError(f'MKDISK -> Ajuste {str(fit).upper()} no reconocido')
        except:
            printError(f'MKDISK -> Ajuste {fit} no reconocido')
        return
    
    mkdisk(path, size, unit, fit)

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
    
    if t[5][-3:] != 'dsk':
        printError(f'RMDISK -> La extension del archivo {t[5]} debe ser .dsk')
        return

    rmdisk(t[5])

#------------------------------------------------------------
#------------------------ FDISK -----------------------------
def p_command_fdisk(t):
    'command_fdisk : FDISK params_fdisk'
    
    required_params = ['path', 'name']

    # Check if exists more than one operation
    op_params = ['delete', 'add']
    op_count = 0
    for param in op_params:
        if param in t[2]:
            op_count += 1
    if op_count > 1:
        printError(f'FDISK -> No se puede usar mas de un parametro entre {op_params}')
        return
    
    # Search the first operation if exists
    op = None
    for param in t[2]:
        if param == 'delete':
            op = 'delete'
            break
        elif param == 'add':
            op = 'add'
            break

    # if not exists operation, add size how required param
    if not op:
        required_params.append('size')

    for param in required_params:
        if param not in t[2]:
            printError(f'FDISK -> Parametro {param} requerido')
            return
        
    path = t[2].get('path')
    size = t[2].get('size', 0)
    unit = t[2].get('unit', 'k')
    name = t[2].get('name')
    type = t[2].get('type', 'p')
    fit = t[2].get('fit', 'wf')
    delete = t[2].get('delete', 'full')
    add = t[2].get('add', 0)

    if unit not in ['b', 'k', 'm']:
        try:
            printError(f'FDISK -> Unidad {str(unit).upper()} no reconocida')
        except:
            printError(f'FDISK -> Unidad {unit} no reconocida')
        return
    
    if size < 0:
        printError(f'FDISK -> Tamaño {size} no valido')
        return
    
    if type not in ['p', 'e', 'l']:
        try:
            printError(f'FDISK -> Tipo {str(type).upper()} no reconocido')
        except:
            printError(f'FDISK -> Tipo {type} no reconocido')
        return
    
    if fit not in ['bf', 'ff', 'wf']:
        try:
            printError(f'FDISK -> Ajuste {str(fit).upper()} no reconocido')
        except:
            printError(f'FDISK -> Ajuste {fit} no reconocido')
        return
    
    if delete != 'full':
        try:
            printError(f'FDISK -> Eliminacion {str(delete).upper()} no reconocida')
        except:
            printError(f'FDISK -> Eliminacion {delete} no reconocida')
        return
    
    if op == 'delete':
        add = None
    elif op == 'add':
        if add == 0:
            printError(f'FDISK -> No se puede agregar 0')
        delete = None
    else:
        delete = None
        add = None
    
    fdisk(path, size, unit, name, type, fit, delete, add)

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
                    | GUION FIT IGUAL CADENA_SC
                    | GUION DELETE IGUAL CADENA_SC
                    | GUION ADD IGUAL ENTERO'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ MOUNT -----------------------------
def p_command_mount(t):
    'command_mount : MOUNT params_mount'
    
    required_params = ['path', 'name']

    for param in required_params:
        if param not in t[2]:
            printError(f'MOUNT -> Parametro {param} requerido')
            return
        
    path = t[2].get('path')
    name = t[2].get('name')

    if path[-3:] != 'dsk':
        printError(f'MOUNT -> La extension del archivo {path} debe ser .dsk')
        return
    
    mount(path, name)

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
def p_command_unmount(t):
    '''command_unmount : UNMOUNT GUION ID IGUAL CADENA
                       | UNMOUNT GUION ID IGUAL CADENA_SC'''
    unmount(t[5])

#------------------------------------------------------------
#------------------------ MKFS ------------------------------
def p_command_mkfs(t):
    '''command_mkfs : MKFS params_mkfs'''

    required_params = ['id']

    for param in required_params:
        if param not in t[2]:
            printError(f'MKFS -> Parametro {param} requerido')
            return
        
    id = t[2].get('id')
    type = t[2].get('type', 'full')
    fs = t[2].get('fs', '2fs')

    if type not in ['full']:
        try:
            printError(f'MKFS -> Tipo {str(type).upper()} no reconocido')
        except:
            printError(f'MKFS -> Tipo {type} no reconocido')
        return
    
    if fs not in ['2fs', '3fs']:
        try:
            printError(f'MKFS -> Sistema de archivos {str(fs).upper()} no reconocido')
        except:
            printError(f'MKFS -> Sistema de archivos {fs} no reconocido')
        return
    
    mkfs(id, fs)

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
                    | GUION TYPE IGUAL CADENA_SC
                    | GUION FS IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ PAUSE -----------------------------
def p_command_pause(t):
    'command_pause : PAUSE'
    pause()

#------------------------------------------------------------
#------------------------ REP -------------------------------
def p_command_rep(t):
    '''command_rep : REP params_rep'''

    required_params = ['name', 'path', 'id']

    name = t[2].get('name')
    path = t[2].get('path')
    id = t[2].get('id')
    ruta = t[2].get('ruta', None)

    if name in ['file', 'ls']:
        required_params.append('ruta')

    for param in required_params:
        if param not in t[2]:
            printError(f'REP -> Parametro {param} requerido')
            return

    if name not in ['mbr', 'disk', 'inode', 'journaling', 'block', 'bm_inode', 'bm_block', 'tree', 'sb', 'file', 'ls']:
        try:
            printError(f'REP -> Reporte {str(name).upper()} no reconocido')
        except:
            printError(f'REP -> Reporte {name} no reconocido')
        return
    
    if path[-3:] not in ['png', 'jpg', 'pdf', 'txt']:
        printError(f'REP -> La extension del archivo {path} debe ser .txt, .png, .jpg o .pdf')
        return
    
    rep(name, path, id, ruta)

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
        printError(f'Sintaxis no válida en la entrada: Token {t.type}, Valor {t.value}, en la linea {t.lexer.lineno}, columna {find_column(t.lexer.lexdata, t)}')
    else:
        printError('Sintaxis no válida en la entrada')

# Build the parser
parser = yacc.yacc()

def get_parser():
    return parser

# entrada = 'rmdisk -path="C:/Users/Usuario/Desktop/entrada.txt"'
# print(parser.parse(entrada))
