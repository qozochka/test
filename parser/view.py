class View:
    """
    Класс используется при взаимодействии с пользователем
    Данные методы используются через контроллеры
    Пока только для вывода различных данных
    """

    def show_data(self, data: dict):
        for row in data.items():
            print(row)

    def show_url(self, data:str):
        return data

    def show_parse_data(self, data: tuple) -> dict:
        addresses_dict = {}
        for item in data:
            for num in range(len(item)):
                if num not in addresses_dict.keys():
                    addresses_dict[num] = []
                addresses_dict[num].append(item[num])

        return addresses_dict
