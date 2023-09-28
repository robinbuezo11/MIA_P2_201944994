def execute(path):
    print('Ejecutando el comando EXECUTE')
    file = open(path, 'r')
    data = file.read()
    return data