""" Модуль соединения с БД """

import sqlite3

connection = sqlite3.connect('./data/data.db')
cursor = connection.cursor()