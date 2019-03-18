import json

def read(path, isJSON=False):
    try:
        f = open(path).read())
        if isJSON != True:
            return f
        try:
            f = json.loads(f)
            return f
        except json.decoder.JSONDecodeError:
            return "JSONDecodeError"
    except FileNotFoundError:
        return "FileNotFoundError"
