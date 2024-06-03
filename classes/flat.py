import re

class Flat():
    def __init__(self, data: list[str]):
        # Получение данных о квартире
        flat_data = data[-2]
        flat_data_arr = flat_data.split(" ")
        self.rooms = flat_data_arr[0].strip()[:1]
        self.area = flat_data_arr[2]
        
        self.location = data[0]
        self.link = data[1]

        # Получение района
        idx = data[0].index("р-н")
        sliced = data[0][idx + 4:]
        idx = sliced.index(",")
        self.district = sliced[0:idx]

        # Получение данных о местоположении (в принципе можно удалить т.к. забагано, но на всякий оставил)
        """  location_data = data[0].split(",")
        self.region = location_data[0]
        self.city = location_data[1].strip()
        district_raw = location_data[2].strip()
        idx = district_raw.index("р-н")
        self.district = district_raw[idx + 3:].strip()
        next = location_data[3]
        try:
            idx = next.index("мкр.")
            self.micro_district = next[idx + 4:].strip()
            self.street = location_data[4].strip() + " " + location_data[5].strip()
        except ValueError:
            self.micro_district = None
            self.street = next.strip() + " " + location_data[4].strip() """


        # Получение цены
        price_sliced = re.findall(r'\b\d+\b', data[-1])
        price_string = ""
        for k in price_sliced:
            price_string += k
        self.price = int(price_string)
    
    def __str__(self):
        return self.location\
        + "\n" + str(self.rooms) + "-комнатная " + str(self.area) + "м²" + ", " + str(self.price) + "р/мес."\
        + "\n" + self.link