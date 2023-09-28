import ply.yacc as yacc
# Import all from lexer
from lexer import *
from Commands.Mkdisk import *
from Commands.Fdisk import *
from Commands.Rep import *

# Grammar rules
def p_init(t):
    'init : list_commands'
    t[0] = t[1]

def p_list_commands(t):
    '''list_commands : list_commands commands
                    | commands'''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_commands(t): 
    '''commands : command_execute
                | command_mkdisk
                | command_fdisk
                | command_rep'''
    t[0] = t[1]

#------------------------------------------------------------
#------------------------ EXECUTE ---------------------------

def p_command_execute(t):
    '''command_execute : EXECUTE GUION PATH IGUAL CADENA
                       | EXECUTE GUION PATH IGUAL CADENA_SC'''
    t[0] = [t[1], t[5]]

#------------------------------------------------------------
#------------------------ MKDISK ----------------------------

def p_command_mkdisk(t):                                       
    'command_mkdisk : MKDISK params_mkdisk'

    required_params = ['path', 'size']
    
    for param in required_params:
        if param not in t[2]:
            print(f'ERROR: MKDISK -> Parametro {param} requerido')
            return
        
    path = t[2].get('path')
    size = t[2].get('size')
    unit = t[2].get('unit', 'M')

    if path[-3:] != 'dsk':
        print(f'ERROR: MKDISK -> La extension del archivo {path} debe ser .dsk')
        return

    if unit not in ['M', 'K']:
        print(f'ERROR: MKDISK -> Unidad {unit} no reconocida')
        return
    
    if size < 0:
        print(f'ERROR: MKDISK -> Tamaño {size} no valido')
        return
    
    mkdisk(path, size, unit)

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
                    | GUION UNIT IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ FDISK -----------------------------

def p_command_fdisk(t):
    'command_fdisk : FDISK params_fdisk'
    
    required_params = ['path', 'size', 'name']

    for param in required_params:
        if param not in t[2]:
            print(f'ERROR: FDISK -> Parametro {param} requerido')
            return
        
    path = t[2].get('path')
    size = t[2].get('size')
    unit = t[2].get('unit', 'K')
    name = t[2].get('name')

    if unit not in ['B', 'K', 'M']:
        print(f'ERROR: FDISK -> Unidad {unit} no reconocida')
        return
    
    if size < 0:
        print(f'ERROR: FDISK -> Tamaño {size} no valido')
        return
    
    fdisk(path, size, unit, name)

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
                    | GUION NAME IGUAL CADENA_SC'''
    t[0] = {t[2]: t[4]}

#------------------------------------------------------------
#------------------------ REP -------------------------------

def p_command_rep(t):
    '''command_rep : REP GUION PATH IGUAL CADENA
                   | REP GUION PATH IGUAL CADENA_SC'''
    rep(t[5])

parser = yacc.yacc()

def get_parser():
    return parser

'''entrada = '''
#execute -path="C:/Users/Usuario/Desktop/entrada.txt"
''' 
print(parser.parse(entrada))
'''