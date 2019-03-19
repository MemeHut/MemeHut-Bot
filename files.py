import json

def read(path, isJSON=False):
    try:
        f = open(path).read()
        if isJSON != True:
            return f
        try:
            f = json.loads(f)
            return f
        except json.decoder.JSONDecodeError:
            return "JSONDecodeError"
        f.close()
    except FileNotFoundError:
        return "FileNotFoundError"


def write(path, content):
    try:
        f = open(path, "w")
        f.write(content)
        print(content)
        f.close()
    except FileNotFoundError:
        return "FileNotFoundError"
