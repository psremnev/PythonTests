import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from Constants import Browsers, ELEMENT_WAIT_TIMEOUT


class DriverHelper:
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

    def get_element_by_css(self, locator, by=By.CSS_SELECTOR):
        try:
            el = self.__driver.find_element(by, locator)
        except Exception as e:
            raise Exception(f'Элемент не найден на странице! {e}')
        return el

    def get_elements_by_css(self, locator, by=By.CSS_SELECTOR):
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
            f"let scroll = document.querySelector('.controls-Scroll-ContainerBase');scroll.scrollTo({el.location.get('x')}, {el.location.get('y')})")

    def get_current_url(self):
        return self.__driver.current_url

    def close_window(self):
        self.__driver.close()

    def el_is_displayed(self, el: WebElement):
        try:
            wait = WebDriverWait(self.__driver, timeout=ELEMENT_WAIT_TIMEOUT)
            visible = wait.until(lambda d: el.is_displayed())
        except:
            visible = False
        return visible

    def el_is_not_displayed(self, el: WebElement):
        return not self.el_is_displayed(el)
