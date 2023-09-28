
from lexer import *



def prueba_archivo(ruta):
    print('------------------')
    print(ruta)
    archivo = open(ruta, 'r')
    data = archivo.read()
    prueba_normal(data)

def prueba_normal(input):
    lexer.input(input)
    while True:
        tok = lexer.token()
        if not tok:  # manejar errores lexicos
            break      # No more input
        print(tok.type, tok.value, tok.lineno, tok.lexpos)

entrada = ''' 
execute -path=C:/Users/Usuario/Desktop/entrada.txt
'''

prueba_normal(entrada)