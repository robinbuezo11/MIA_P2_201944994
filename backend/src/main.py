from Utils.Utilities import *
from Utils.Fmanager import * 
from parser_ import *

print()
printSuccess("Robin Omar Buezo Díaz")
printSuccess("201944994\n")

printConsole(" *** Bienvenido al sistema de archivos *** ")

parser = get_parser()
while True:
   entrada = input('\033[36m>> Ingrese un comando\n\033[00m')
   print()
   parse_result = parser.parse(entrada)