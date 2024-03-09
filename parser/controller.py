from parser.dataparsing import DataParsing
from parser.db_connection import DBConnection
from parser.view import View


class Controller:
    '''
    Данный класс отвечает за запуск и обработку всей программы.
    Является связующим звеном всех остальных классов и методов
    '''
    def __init__(self):
        self.parser = DataParsing()
        self.model = DBConnection()
        self.view = View()

    def create_table(self):
        self.model.create_table()

    def show_all_urls(self):
        self.view.show_data(self.model.select_urls())

    def show_url_by_user_id(self, user_id):
        return self.view.show_url(self.model.select_url_by_user_id(user_id))

    def add_user_url(self, user_id, url):
        self.model.insert_data(user_id, url)

    def parsing_url(self, rooms, location, **filter_settings):
        return self.parser.get_url_list(rooms, location, **filter_settings)

    def parsing_from_url(self, user_id):
        data = self.parser.get_parsed_data(self.model.select_url_by_user_id(user_id)[1])
        return self.view.show_parse_data(data)
