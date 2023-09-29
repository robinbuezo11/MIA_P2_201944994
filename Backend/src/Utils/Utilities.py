def printConsole(text): print("\033[36m>> {}\033[00m" .format(text))

def printError(error): print("\033[91m<<Error>> {}\033[00m" .format(error))

def printSuccess(success): print("\033[1;32m>> {}\033[00m" .format(success))

def printWarning(question="¿Estás seguro? (s/n): "):
      confirm = input("\033[1;33m<<Confirm>> {}\033[00m\n" .format(question))
      return confirm.lower() == "s"
   
def coding_str(string,size):
    return string.encode('utf-8')[:size].ljust(size, b'\0')

def get_sizeB(size,unit):
    return size if unit == "b" else (size * 1024 if unit == "k" else size * 1024 * 1024 )

def get_sizeM(size,unit):
    return size if unit == "m" else (int(size/1024) if unit == "k" else int(size/1024/1024))