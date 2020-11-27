import uuid

def Invoice(name, id,):
    uid = str(uuid.uuid1())[:8].upper()
    return f'{name}-{id}-{uid}'
