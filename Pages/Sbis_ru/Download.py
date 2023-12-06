import requests
from selenium.webdriver.common.by import By
from sys import platform
from selenium.webdriver.support.wait import WebDriverWait

from Constants import Platform, ELEMENT_WAIT_TIMEOUT, STATUS_OK


class Download:
    url = 'https://sbis.ru/download'

    def __init__(self, dr_helper):
        self.dr_helper = dr_helper

    def open(self):
        self.dr_helper.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        self.plugin_tab = self.find_tab('СБИС Плагин')

    def find_tab(self, tab_name):
        tabs = self.dr_helper.get_elements_by_css('.controls-TabButton')
        for tab in tabs:
            tab_caption_el = tab.find_element(By.CSS_SELECTOR, '.controls-TabButton__caption')
            if tab_caption_el.text == tab_name:
                return tab

    def get_tab_by_platform(self):
        if platform == "linux" or platform == "linux2":
            tab_name = Platform.Linux
        elif platform == "darwin":
            tab_name = Platform.MACOS
        elif platform == "win32":
            tab_name = Platform.WINDOWS

        return self.find_tab(tab_name.value)

    def find_first_link_for_download(self):
        return self.dr_helper.get_elements_by_css('Скача', By.PARTIAL_LINK_TEXT)[0]

    @staticmethod
    def download_file_by_link(url):
        response = requests.get(url)
        if response.status_code == STATUS_OK:
            file_size = round(int(response.headers.get("Content-Length", 0)) / 1024 / 1024, 2)
        else:
            raise Exception(f'Не удалось загрузить файл: {response.reason}')
        return [response.content, str(file_size)]

    @staticmethod
    def save_file(content):
        f = open('plugin.exe', 'wb')
        f.write(content)
        f.close()
