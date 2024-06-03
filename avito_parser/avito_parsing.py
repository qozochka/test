import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class AvitoParsing:
    """
    Класс парсера, который ставит своей целью получить ссылку авито именно с
    параметрами пользователя.
    """

    def __init__(self, location: list, rooms: int, cost_min: int, cost_max: int, without_commission: bool,
                 without_deposit: bool, driver, actions):
        """
        Инициализация объекта
        :param location: list, где 0 элемент - город, а 1 элемент - район.
        :param without_commission: bool, поле-чекбокс "Без комиссии", True - выбор этого чекбокса
        :param without_deposit: bool, поле-чекбокс "Без залога", True - выбор этого чекбокса.
        """
        self.driver = driver
        self.district_code = None
        self.actions = actions
        self.user_url = None
        self.district: str = location[1]
        self.city: str = (location[0]).title()
        self.URL = "https://www.avito.ru/krasnoyarsk/nedvizhimost"
        self.location: list = location
        self.rooms = rooms
        self.cost_min = cost_min
        self.cost_max = cost_max
        self.without_comission = without_commission
        self.without_deposit = without_deposit

    def get_user_city(self):
        """
        Метод для ввода города на авито
        """
        time.sleep(4)
        city_element = self.driver.find_element(By.XPATH,
                                                "//span[@class='desktop-nev1ty' and contains(text(), '{}')]".format(
                                                    self.city))
        self.actions.move_to_element(city_element).click().perform()
        time.sleep(15)
        user_city = self.driver.find_element(By.CSS_SELECTOR,
                                             "input.styles-module-searchInput-DS602[placeholder='Город или регион']")
        self.actions.move_to_element(user_city).click().perform()
        user_city.clear()
        time.sleep(3)
        user_city.send_keys(self.city)
        time.sleep(5)
        city_button = self.driver.find_element(By.XPATH,
                                               f"//button[@type='button']//strong[contains(text(), {self.city})][not("
                                               f"preceding-sibling::text())][not(following-sibling::text())]")
        self.actions.move_to_element(city_button).click().perform()

        time.sleep(2)
        districts_tab = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Районы')]")

        self.actions.move_to_element(districts_tab).click().perform()
        time.sleep(1.5)

        district_checkboxes = self.driver.find_elements(By.XPATH, "//label[@role='checkbox']")
        self.district_code = None
        for checkbox in district_checkboxes:
            district_name = checkbox.find_element(By.XPATH,
                                                  ".//div[@class='styles-module-label-T3Wr6 "
                                                  "styles-module-label_end-QqXEL']")
            if district_name.text.strip() == self.district:
                self.district_code = checkbox.get_attribute('data-marker').split('/')[-1]
                self.actions.move_to_element(district_name).click().perform()
                time.sleep(1)
                show_button = self.driver.find_element(By.CSS_SELECTOR,
                                                       "button[data-marker='popup-location/save-button']")
                self.actions.move_to_element(show_button).click().perform()
                break

    def get_district_code(self):
        """
        Метод для ввода района пользователя
        """
        time.sleep(10)

        city_element = self.driver.find_element(By.XPATH,
                                                "//span[@class='desktop-nev1ty' and contains(text(), '{}')]".format(
                                                    self.city))
        self.actions.move_to_element(city_element).click().perform()
        time.sleep(5)

        districts_tab = self.driver.find_element(By.XPATH, "//span[contains(text(),'Районы')]")

        self.actions.move_to_element(districts_tab).click().perform()
        time.sleep(1.5)

        # Получаем все чекбоксы районов
        district_checkboxes = self.driver.find_elements(By.XPATH, "//label[@role='checkbox']")

        # Ищем нужный район и извлекаем его код
        self.district_code = None
        for checkbox in district_checkboxes:
            district_name = checkbox.find_element(By.XPATH,
                                                  ".//div[@class='styles-module-label-T3Wr6 "
                                                  "styles-module-label_end-QqXEL']")
            if district_name.text.strip() == self.district:
                self.district_code = checkbox.get_attribute('data-marker').split('/')[-1]
                self.actions.move_to_element(district_name).click().perform()
                time.sleep(1)
                show_button = self.driver.find_element(By.CSS_SELECTOR,
                                                       "button[data-marker='popup-location/save-button']")
                self.actions.move_to_element(show_button).click().perform()
                break

    def send_keys_slowly(self, element, text, delay=0.1):
        """Отправляет символы по одному с задержкой."""
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

    def get_filters(self):
        """
        Выставляет фильтры на сайте, в зависимости от выбора пользователя

        """
        self.driver.get(self.URL)
        time.sleep(2)
        self.get_user_city()

        time.sleep(2)
        rent_button = self.driver.find_element(By.XPATH,
                                               "//span[@data-category-id='24' and contains(text(), 'Снять "
                                               "долгосрочно')]")

        self.actions.move_to_element(rent_button).click().perform()
        time.sleep(1)
        flats = self.driver.find_element(By.CSS_SELECTOR,
                                         "li.rubricator-list-item-item-WKnEv[data-marker='category[25934]']")
        time.sleep(1)

        self.actions.move_to_element(flats).click().perform()

        rooms_option = WebDriverWait(self.driver, 13).until(
            EC.element_to_be_clickable((By.XPATH,
                                        f"//label[@class='styles-module-root-_klXj styles-module-root_size_m-dJpjI "
                                        f"styles-module-root_fullWidth-_6hXZ' and @data-marker='params["
                                        f"550]/checkbox/570{self.rooms + 2}']"))
        )
        self.actions.move_to_element(rooms_option).click().perform()
        time.sleep(3)
        cost_min_but = self.driver.find_element(By.CSS_SELECTOR,
                                                "input.styles-module-input-Lisnt[data-marker='price-from/input']")
        self.actions.move_to_element(cost_min_but).click().perform()
        time.sleep(1)
        cost_min_but.clear()  # Очистка поля ввода
        self.send_keys_slowly(cost_min_but, str(self.cost_min))
        cost_max_but = self.driver.find_element(By.CSS_SELECTOR,
                                                ".styles-module-inputWrapper-yFW0m .styles-module-input-Lisnt["
                                                "data-marker='price-to/input']")
        time.sleep(1)
        self.actions.move_to_element(cost_max_but).click().perform()
        time.sleep(1)
        cost_max_but.clear()  # Очистка поля ввода
        self.send_keys_slowly(cost_max_but, str(self.cost_max))
        time.sleep(1.3)

        if self.without_comission:
            commission = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "label.styles-module-root-_klXj[data-marker='params[122383]/checkbox/1']")))
            self.actions.move_to_element(commission).click().perform()
            time.sleep(1)
        if self.without_deposit:
            deposit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "label.styles-module-root-_klXj[data-marker='params[122382]/checkbox/1']")))
            self.actions.move_to_element(deposit).click().perform()
            time.sleep(0.5)
        button_show = self.driver.find_element(By.CSS_SELECTOR,
                                               "button[data-marker='search-filters/submit-button'][type='button']")

        self.actions.move_to_element(button_show).click().perform()
        self.get_district_code()
        time.sleep(2)
        self.user_url = self.driver.current_url
        time.sleep(2)

    def get_user_url(self):
        self.get_filters()
        return self.user_url


    def close(self):
        self.driver.close()
        time.sleep(2)

