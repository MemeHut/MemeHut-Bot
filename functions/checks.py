def isInt(str):
    try:
        inT = int(str)
        return True
    except ValueError:
        return False
