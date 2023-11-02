from Utils.Globals import *

def logout():
    if len(user_session) == 0:
        return False, f'No hay una sesión iniciada\n'
    
    user_session.pop()
    return True, f'Se cerró sesión correctamente\n'