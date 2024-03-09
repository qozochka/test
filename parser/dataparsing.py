from urllib.request import urlopen

from bs4 import BeautifulSoup
from cianparser import CianParser


class DataParsing:
    """
    Класс обрабатывает парсинг ссылки с фильтрами с циан
    для этого используется метод get_url_list
    """

    def __init__(self):
        self.filter_settings = None
        self.rooms = None
        self.location = None

    def get_url_list(self, rooms, location, **filter_settings):
        """
        Метод запускает фильтры и возвращает ссылку на циан с готовыми фильтрами
        :return:
        """
        self.location = location
        self.filter_settings = filter_settings
        self.rooms = rooms
        parser = CianParser(location=self.location)
        data = parser.get_flats(deal_type="rent_long", rooms=self.rooms,
                                additional_settings=self.filter_settings)
        return parser.url_list

    def get_parsed_data(self, url):
        data = self.ParserFromPage(url)
        return data.parse()

    class ParserFromPage:
        def __init__(self, url):
            self.url = url
            self.soup = BeautifulSoup(urlopen(self.url), 'lxml')

        def parse(self):
            divs = self.soup.find_all('div', class_="_93444fe79c--card--ibP42")
            addresses_list = []
            addresses_url = []
            addresses_description = []
            addresses_price = []

            for div in divs:
                address_string = ''
                addresses = div.find_all('div', class_="_93444fe79c--labels--L8WyJ")
                for address in addresses:
                    address_string += address.text
                addresses_list.append(address_string)

                addresses_url.append(div.find('a', class_="_93444fe79c--link--VtWj6").attrs['href'])
                addresses_description.append(div.find('span',
                                                      class_="_93444fe79c--color_black_100--Ephi7 "
                                                             "_93444fe79c--lineHeight_28px--KFXmc "
                                                             "_93444fe79c--fontWeight_bold--BbhnX "
                                                             "_93444fe79c--fontSize_22px--sFuaL "
                                                             "_93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY "
                                                             "_93444fe79c--text_letterSpacing__normal--tfToq").text)
                addresses_price.append(div.find('div',
                                                class_="_93444fe79c--container--aWzpE").text)

            return addresses_list, addresses_url, addresses_description, addresses_price
