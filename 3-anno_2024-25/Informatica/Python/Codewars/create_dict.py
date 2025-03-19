'''
--- VECCHIA VERSIONE ---

def create_dict(keys, values):
    i = 0; d = {}
    d[key] = (values[i] if i<len(values) else None); i += 1 for key in keys 
    return d
'''
def create_dict(keys, values):
    return {key: values[i] if i < len(values) else None for i, key in enumerate(keys)}
