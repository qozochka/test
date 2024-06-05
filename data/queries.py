""" Модуль предустановленных команд для работой с БД """

from sqlite3 import Error as DbError
from data.database import cursor, connection
from data.tables import users


def initialize_database() -> bool:
    """ Создаёт таблицы """
    try:
        cursor.execute(users)
        return True
    except DbError as err:
        print(err)
        return False


def get_ids():
    """ Получает id всех юзеров """
    data = cursor.execute("SELECT id FROM users")
    return data.fetchone()


def get_settings(id):
    """ Получает настройки пользователя """
    try:
        data = cursor.execute("SELECT settings FROM users WHERE id = ?", (id, ))
        return data.fetchone()[0]
    except DbError as err:
        print(err)
        return None


def save_settings(id, location_settings) -> bool:
    """ Сохраняет все настройки пользователя """
    try:
        cursor.execute("UPDATE users SET settings = ? WHERE id = ?", (location_settings, id))
        connection.commit()
        return True
    except DbError as err:
        print(err)
        return False


def get_newest_cian_id(id) -> int:
    """ Получает сохранённое id самой новой квартиры с Циана """
    data = cursor.execute("SELECT cian_first_id FROM users WHERE id = ?", (id, ))
    return data.fetchone()[0]


def save_newest_cian_id(id, cian_first_id) -> bool:
    """ Сохраняет id самой новой квартиры с Циана """
    cursor.execute("UPDATE users SET cian_first_id = ? WHERE id = ?", (cian_first_id, id))
    connection.commit()
    return True


def get_current_cian_page(id):
    """ Получает текущую страницу Циана """
    data = cursor.execute("SELECT cian_page FROM users WHERE id = ?", (id, ))
    return data.fetchone()[0]


def save_current_cian_page(id, page) -> bool:
    """ Сохраняет текущую страницу Циана """
    cursor.execute("UPDATE users SET cian_page = ? WHERE id = ?", (page, id))
    connection.commit()
    return True


def get_current_array_page(id) -> int:
    """ Получает текущую страницу массива"""
    try:
        data = cursor.execute("SELECT array_page FROM users WHERE id = ?", (id, ))
        return data.fetchone()[0]
    except DbError as err:
        print(err)
        return False


def save_current_array_page(id, page) -> bool:
    """ Сохраняет текущую страницу массива """
    try:
        cursor.execute("UPDATE users SET array_page = ? WHERE id = ?", (page, id))
        connection.commit()
        return True
    except DbError as err:
        print(err)
        return False


def save_user(id) -> bool:
    """ Сохраняет пользователя в БД """
    try:
        cursor.execute("INSERT OR IGNORE INTO users(id) VALUES(?)", (id, ))
        connection.commit()
        return True
    except DbError as err:
        print(err)
        return False
    

def get_current_avito_page(id):
    """ Получает текущую страницу Авито """
    data = cursor.execute("SELECT avito_page FROM users WHERE id = ?", (id, ))
    return data.fetchone()[0]


def save_current_avito_page(id, page) -> bool:
    """ Сохраняет текущую страницу Авито """
    cursor.execute("UPDATE users SET avito_page = ? WHERE id = ?", (page, id))
    connection.commit()
    return True