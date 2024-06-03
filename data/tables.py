""" Модуль с таблицами для БД """

users = """CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    settings TEXT DEFAULT NULL,
    array_page INT DEFAULT 1,
    cian_page INT DEFAULT 1
)"""