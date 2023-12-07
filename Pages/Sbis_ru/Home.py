from selenium.webdriver.common.by import By
from Pages.Base import Base


class Home(Base):
    url = 'https://sbis.ru/'

    def open(self):
        self.dr_helper.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        _, self.contacts_btn, _ = self.dr_helper.get_elements_by_css('.sbisru-Header__menu-link')
        self.download_btn = self.dr_helper.get_elements_by_css('Скачать СБИС', By.LINK_TEXT)[0]
