from cianparser import CianParser


class DataParsing:
    """
    Класс обрабатывает парсинг ссылки с фильтрами с циан
    для этого используется метод get_url_list
    """

    def __init__(self, rooms, location, **filter_settings):
        self.location = location
        self.filter_settings = filter_settings
        self.rooms = rooms
        pass



    def get_url_list(self):
        """
        запускает фильтры и возвращает ссылку на циан с готовыми фильтрами
        :return:
        """
        parser = CianParser(location=self.location)
        data = parser.get_flats(deal_type="rent_long", rooms=self.rooms,
                                additional_settings=self.filter_settings)
        return parser.url_list
