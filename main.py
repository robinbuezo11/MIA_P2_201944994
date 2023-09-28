import os
from Utils.load import * 
from parser_ import *
from Commands.Execute import execute

if __name__ == "__main__":
   print("=============CONSOLA DE COMANDOS================")
   print("DIRECTORIO ACTUAL:", os.getcwd())
   print("================================================")

   parser = get_parser()
   while True:
         try:
            entrada = input('>> ')
            parse_result = parser.parse(entrada)
            if isinstance(parse_result, list):
               if isinstance(parse_result[0], list):
                  for parse_res in parse_result:
                     if parse_res[0] == 'execute':
                        data = execute(parse_res[1])
                        parse_res = parser.parse(data)
         except EOFError:
            break