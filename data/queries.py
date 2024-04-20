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



def save_user(id) -> bool:
    """ Сохраняет пользователя в БД """
    try:
        cursor.execute("INSERT OR IGNORE INTO users(id) VALUES(?)", (id, ))
        connection.commit()
        return True
    except DbError as err:
        print(err)
        return False