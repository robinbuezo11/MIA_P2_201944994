# import ply
import ply.lex as lex
from Utils.Utilities import *

# List of errors
errors = []

# Reserved words
reserved = {
    'execute' : 'EXECUTE',
    'mkdisk' : 'MKDISK',
    'rmdisk' : 'RMDISK',
    'fdisk' : 'FDISK',
    'mount' : 'MOUNT',
    'unmount' : 'UNMOUNT',
    'mkfs' : 'MKFS',

    'pause' : 'PAUSE',
    'rep' : 'REP',

    'path' : 'PATH',
    'size' : 'SIZE',
    'unit' : 'UNIT',
    'fit'  : 'FIT',
    'name' : 'NAME',
    'type' : 'TYPE',
    'delete' : 'DELETE',
    'add' : 'ADD',
    'id' : 'ID',
    'ruta' : 'RUTA',
    'fs' : 'FS',
}

# List of global token names.   This is always required
tokens = [
    'IGUAL',
    'GUION',
    'ENTERO',
    'CADENA',
    'CADENA_SC',
    'COMMENT'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_IGUAL = r'\='
t_GUION = r'\-'

# Regular expression rules with some action code
#   All values are returned as strings

def t_ENTERO(t):
    r'-?\d+\b'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\"(.|\n)*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CADENA_SC(t):
    r'[a-zA-Z0-9_/.,:][a-zA-Z0-9_/.,:]*'
    t.value = t.value.lower()
    t.type = reserved.get(t.value, 'CADENA_SC') # Check for reserved words
    return t

def t_COMMENT(t):
    r'\#.*?(?=\n|$|\r)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters and empty lines
t_ignore = ' \t'
#t_ignore_empty_line = r'\n\s*\n+'

# Error handling rule
def t_error(t):
    errors.append(t.value[0])
    printError(f'Caracter no reconocido: {t.value[0]} en la linea {t.lexer.lineno}, columna {find_column(t.lexer.lexdata, t)}, se omitirá')
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Build the lexer
lexer = lex.lex()
