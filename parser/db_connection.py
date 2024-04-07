"""
Модуль содержит класс DBConnection, который используется для связи с json файлами
"""
import json
import os

from config import USERS_URLS_FILENAME


class DBConnection:
    """
    Данный класс обрабатывает все запросы для файлов json
    в нём реализуются методы для каждой задачи, необходимой в работе с json
    """

    def insert_data(self, user_id: int, url: str):
        """
        Метод позволяет заполнить json файл данными в виде user_id и url
        """
        if os.path.exists(USERS_URLS_FILENAME) and os.path.getsize(USERS_URLS_FILENAME) > 0:
            with open(USERS_URLS_FILENAME, "r") as fh:
                data = json.load(fh)

            with open(USERS_URLS_FILENAME, "w") as fh:
                data[user_id] = url
                json.dump(data, fh, indent=4)
        else:
            with open(USERS_URLS_FILENAME, "w") as fh:
                data = {user_id: url}
                json.dump(data, fh, indent=4)

    def select_urls(self):
        """
        Метод используется для получения всех ссылок из файла users_urls.json
        Возвращает список кортежей (user_id, url)
        :return rows:
        """
        if os.path.exists(USERS_URLS_FILENAME) and os.path.getsize(USERS_URLS_FILENAME) > 0:
            with open(USERS_URLS_FILENAME, "r+") as fh:
                data = json.load(fh)
                return data
        else:
            print("u dont have a users_urls")

    def select_url_by_user_id(self, user_id):
        """
        Метод используется для получения ссылки по user_id из users_urls.json
        Возвращает список кортежей (user_id, url)
        :return rows:
        """
        data = self.select_urls()
        if len(data) != 0:
            for row in data.items():
                if int(row[0]) == user_id:
                    return row
        else:
            print("u dont have a users_urls")
