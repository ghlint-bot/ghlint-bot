import json

def load_json_file(path: str) -> json:
    file = open(path, 'r')
    data: json = json.loads(file.read())
    file.close()
    return data

