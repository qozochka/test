import requests
from bs4 import BeautifulSoup


class AvitoParsing:
    def __init__(self):
        self.district_code = None
        self.user_url = None
        self.district: str = ''
        self.city: str = ''
        self.URL = "https://www.avito.ru/"
        self.location: list = []
        self.rooms = None

    def get_location(self, location):
        self.location = location
        self.city = location[0]
        self.district = location[1]
        cookies = {
            'sessid': 'b9c66ffddbdff38f6308e6fc4b7a4cdf.1715533824',}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

        response = requests.get(f"https://www.avito.ru/{self.city}", cookies=cookies,headers=headers)

        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')
        district_tags = soup.find_all('label', {'role': 'checkbox'})

        for tag in district_tags:
            district_name = tag.find('div',
                                     class_='styles-module-label-T3Wr6 styles-module-label_end-QqXEL').text.strip()
            if district_name == self.district:
                self.district_code = tag['data-marker'].split('/')[-1]
                return self.district_code

    def get_user_url(self, location, rooms):
        self.get_location(location)
        self.rooms = rooms
        self.user_url = self.URL + self.city + f"?district={self.district_code}"
        return self.user_url


a = AvitoParsing()
print(a.get_user_url(["krasnoyarsk", "Железнодорожный"], 3))
