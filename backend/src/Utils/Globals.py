mounted_partitions = []
user_session = []

def display_mounted_partitions():
    result = "\n***** Particiones montadas *****\n"
    if len(mounted_partitions) == 0:
        result += 'No hay particiones montadas\n'
        return result
    for data in mounted_partitions:
        result += f'ID: {data["id"]}\n'
        # print(f'Path: {data["path"]}')
        # print(f'Nombre: {data["name"]}')
        result += f'PARTICION:\n'
        result += data["partition"].display_info()
        result += '-'*25 + '\n'
    return result

def get_mounted_partitionbyId(id):
    for data in mounted_partitions:
        if data['id'].lower() == id.lower():
            return data
    return None

