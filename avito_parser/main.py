
from selenium.webdriver import ActionChains
from avito_parsing import AvitoParsing
from Parser import Parser
from ConnectionJs import ConectionJs
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = uc.Chrome(options=options)
actions = ActionChains(driver)




if __name__ == "__main__":
    for_url = AvitoParsing(['Красноярск', 'Октябрьский'], 0, 0, 50000, True, False, driver, actions)
    user_url = for_url.get_user_url()
    connectionJs = ConectionJs()
    connectionJs.insert_data(178524, user_url)
    parser = Parser(user_url, driver, actions, 1)
    parser.get_items()
    print("".join(parser.format_data()))
    parser.close()





