mounted_partitions = []
user_session = None

def display_mounted_partitions():
    print('\n***** Particiones montadas *****')
    if len(mounted_partitions) == 0:
        print('No hay particiones montadas')
        return
    for data in mounted_partitions:
        print(f'ID: {data["id"]}')
        # print(f'Path: {data["path"]}')
        # print(f'Nombre: {data["name"]}')
        print(f'PARTICION:')
        data["partition"].display_info()
        print()

def get_mounted_partitionbyId(id):
    for data in mounted_partitions:
        if data['id'].lower() == id.lower():
            return data
    return None