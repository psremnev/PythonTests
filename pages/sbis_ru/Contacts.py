from pages.Base import Base
from selenium.webdriver.common.by import By

class Contacts(Base):
    url = 'https://sbis.ru/contacts'

    def open(self):
        self.dr.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        self.header = self.dr.get_element_by('//h1[text()="Контакты"]', By.XPATH)
        self.banner = self.dr.get_element_by('.sbisru-Contacts__logo-tensor')
        self.current_region = self.dr.get_element_by('.sbis_ru-Region-Chooser__text')
        self.city_list = self.dr.get_element_by('.sbisru-Contacts-City__col')
        self.partners_city_list = self.dr.get_element_by('.sbisru-Contacts-List__col')
        self.region_items_header = self.dr.get_elements_by('.sbisru-Contacts-List__city')

    def has_city_in_partners_list(self, region):
        if not region:
            return Exception('Не указан параметр region')
        if not self.region_items_header:
            return Exception('Отсутствуют регионы партнера в списке')

        for partner_region in self.region_items_header:
            if partner_region.text == region:
                return True
        return False
