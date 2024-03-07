"""
Модуль содержит класс DBConnection, который используется для связи с бд
"""
from mysql.connector import connect, Error

from config import host, user, password, database


class DBConnection:
    def __init__(self):
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password
            ) as connection:
                create_db_query = "CREATE DATABASE IF NOT EXISTS db"
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query)
                    connection.commit()
        except Error as e:
            print(e)

    def create_table(self):
        """
        Метод создаёт таблицу (если такой ещё не существует)
        Временно создаётся таблица, которая хранит id из telegram и url-адрес
        :return:
        """
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                try:
                    # create table
                    with connection.cursor() as cursor:
                        create_table_query = """
                        CREATE TABLE IF NOT EXISTS users_urls(
                        user_id INT NOT NULL PRIMARY KEY,
                        url TEXT
                        )
                        """
                        cursor.execute(create_table_query)
                        connection.commit()
                        print("Table created successfully")
                finally:
                    connection.close()

        except Error as ex:
            print("Connection refused...")
            print(ex)

    def drop_table(self):
        """
        Метод удаляет таблицу, пока, которую задали вручную
        :return:
        """
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                try:
                    # drop table
                    with connection.cursor() as cursor:
                        create_table_query = """
                        DROP TABLE IF EXISTS users_urls
                        """
                        cursor.execute(create_table_query)
                        connection.commit()
                        print("Table deleted successfully")
                finally:
                    connection.close()

        except Error as ex:
            print("Connection refused...")
            print(ex)

    def insert_data(self, user_id, url):
        """
        Метод позволяет заполнить таблицу users данными в виде user_id и url
        """
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                try:
                    # insert data
                    with connection.cursor() as cursor:
                        insert_query = "INSERT INTO users_urls (user_id, url) VALUES (%s, %s)"
                        cursor.execute(insert_query, (user_id, url))
                        connection.commit()
                        print('Data insert successfully completed')
                finally:
                    connection.close()

        except Error as ex:
            print("Connection refused...")
            print(ex)

    def select_data(self):
        """
        Метод используется для получения данных из таблицы users
        Возвращает список кортежей (user_id, url)
        :return rows:
        """
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                try:
                    # select data
                    with connection.cursor() as cursor:
                        select_query = 'SELECT * FROM users_urls'
                        cursor.execute(select_query)

                        rows = cursor.fetchall()
                finally:
                    connection.close()
                    return rows

        except Error as ex:
            print("Connection refused...")
            print(ex)
