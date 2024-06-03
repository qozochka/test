import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Parser:
    def __init__(self, user_url: str, driver, actions, count=1):
        self.user_url = user_url
        self.driver = driver
        self.count = count
        self.actions = actions
        self.info_titles = []
        self.info_urls = []
        self.info_prices = []
        self.info_descriptions = []
        self.info_addresses = []

    def get_items(self):
        self.driver.get(self.user_url)
        time.sleep(5)
        while self.count > 0:
            self.parse_page()
            next_page_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                          "a[data-marker='pagination-button/nextPage']")
            if next_page_buttons:
                next_page_button = next_page_buttons[0]
                self.actions.move_to_element(next_page_button).click().perform()
                time.sleep(2)
            else:
                break

            self.count -= 1

    def parse_page(self):
        amount_of_flats = int(self.driver.find_element(By.CSS_SELECTOR, "[data-marker='page-title/count']").text)
        count = 0

        time.sleep(3)
        flats = self.driver.find_elements(By.CSS_SELECTOR, "div[data-marker='item']")
        for flat in flats:
            if count == amount_of_flats:
                break
            try:
                self.info_titles.append(flat.find_element(By.CSS_SELECTOR, "[itemprop='name']").text)
            except NoSuchElementException:
                self.info_titles.append("Название отсутствует")
            try:
                self.info_urls.append(flat.find_element(By.CSS_SELECTOR, "[itemprop='url']").get_attribute("href"))
            except NoSuchElementException:
                self.info_urls.append("Ссылка отсутствует")
            try:
                self.info_prices.append(
                    flat.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content"))
            except NoSuchElementException:
                self.info_prices.append("Цена отсутствует")
            try:
                self.info_descriptions.append(
                    flat.find_element(By.XPATH, ".//div[@class='iva-item-descriptionStep-C0ty1']/p").text)
            except NoSuchElementException:
                self.info_descriptions.append("Описание отсутствует")
            try:
                address_element = flat.find_element(By.XPATH,
                                                    ".//div[@data-marker='item-address']")

                self.info_addresses.append(address_element.text)
            except NoSuchElementException:
                self.info_addresses.append("Адрес отсутствует")
            time.sleep(1)
            count += 1

        return self.info_titles, self.info_urls, self.info_prices, self.info_addresses

    def format_data(self):
        formatted_data = []
        c = 1
        for title, address, price, description, url in zip(self.info_titles, self.info_addresses, self.info_prices,
                                                           self.info_descriptions,
                                                           self.info_urls):
            formatted_data.append(f"{c}. {title},\nАдрес: {address},\nСтоимость: {price},\nОписание: "
                                  f"{description}\n{url}\n")
            c += 1
        return formatted_data

    def close(self):
        self.driver.close()
        time.sleep(2)
