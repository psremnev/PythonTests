from selenium.webdriver.common.by import By
from pages.Base import Base


class Home(Base):
    url = 'https://sbis.ru/'

    def open(self):
        self.dr.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        _, self.contacts_popup_btn, _, _ = self.dr.get_elements_by('.sbisru-Header__menu-link')
        self.download_btn = self.dr.get_elements_by('//a[@href="/download"]', By.XPATH)
