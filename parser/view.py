class View:
    """
    Класс используется при взаимодействии с пользователем
    Данные методы используются через контроллеры
    Пока только для вывода различных данных

    """

    def show_data(self, data):
        for row in data:
            print(row)

    def show_url(self, data):
        return data

    def show_parse_data(self, data):
        return data
