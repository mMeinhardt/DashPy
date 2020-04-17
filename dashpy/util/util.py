

def to_bytes(data, encoding='utf-8'):
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode(encoding)
    else:
        raise TypeError('Neither string of byte object')

