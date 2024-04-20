

def isInteger(value) -> bool:
    try:
        value = int(value)
        return True
    except:
        return False