from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from constants import Browsers, ELEMENT_WAIT_TIMEOUT
from selenium.webdriver.support import expected_conditions as EC

error_el = 'Элемент не найден на странице!'


class Driver:
    __browser = Browsers.Chrome
    __driver = None

    def __init__(self, browser=Browsers.Chrome):
        self.__browser = browser

    def quit(self):
        if self.__driver:
            self.__driver.quit()

    def get_driver(self):
        return self.__driver

    def init_driver(self):
        if not self.__driver:
            match self.__browser:
                case Browsers.Chrome:
                    self.__driver = webdriver.Chrome()
                case Browsers.FireFox:
                    self.__driver = webdriver.Firefox()

    def open(self, url):
        self.init_driver()
        self.__driver.get(url)
        self.__driver.maximize_window()

    def get_element_by(self, locator, by=By.CSS_SELECTOR):
        try:
            el_is_exist, el = self.el_is_displayed(locator, by)
            if el_is_exist:
                return el
            else:
                raise Exception({error_el})
        except Exception as e:
            raise Exception(f'{error_el} {e}')

    def get_elements_by(self, locator, by=By.CSS_SELECTOR):
        try:
            el = self.__driver.find_elements(by, locator)
        except Exception as e:
            raise Exception(f'Коллекция элементов не найдена на странице! {e}')
        return el

    def get_current_window(self):
        return self.__driver.current_window_handle

    def switch_to_window(self, window):
        return self.__driver.switch_to.window(window)

    def get_windows(self):
        return self.__driver.window_handles

    def scroll_to_el(self, el):
        # тут нужно сделать относительно конкретного элемента так как сролл контейнеров может быть много,
        # но пока не стал делать в рамках тестового
        self.__driver.execute_script(
            f"const scroll = document.querySelector('.controls-Scroll-ContainerBase');scroll.scrollTo({el.location.get('x')}, {el.location.get('y')})")

    def scroll_to_el_by_css(self, selector):
        self.__driver.execute_script(f"const scroll = document.querySelector('.controls-Scroll-ContainerBase');const el = document.querySelector('.tensor_ru-Index__card').getBoundingClientRect();scroll.scrollTo(el.x, el.y)")

    def get_current_url(self):
        return self.__driver.current_url

    def close_window(self):
        self.__driver.close()

    def el_is_displayed(self, locator, by=By.CSS_SELECTOR):
        try:
            wait = WebDriverWait(self.__driver, timeout=ELEMENT_WAIT_TIMEOUT)
            el = wait.until(EC.visibility_of_element_located((by, locator)))
            visible = isinstance(el, WebElement)
        except Exception as e:
            raise Exception(f"{error_el}, {e}")

        return visible, el

    def el_is_not_displayed(self, el: WebElement):
        return not self.el_is_displayed(el)
