""" Модуль с вспомогательными функциями """


def isInteger(value: str | int) -> bool:
    """ Проверяет, является ли value целым числом """
    try:
        value = int(value)
        return True
    except:
        return False
