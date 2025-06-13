from selenium.webdriver.common.by import By
from pages.Base import Base

class Home(Base):
    url = 'https://tensor.ru/'

    def open(self):
        self.dr.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        self.power_in_people_card, self.power_in_people_card_title = self.find_power_in_people_card()
        self.power_in_people_card_more = self.power_in_people_card.find_element(By.LINK_TEXT, 'Подробнее')

    def power_in_people_card_title_is_visible(self):
        return self.power_in_people_card_title.is_displayed() and self.power_in_people_card_title.text == 'Сила в людях'
    def find_power_in_people_card(self):
        # для инициализации элемента нужно проскролить
        self.dr.scroll_to_el_by_css('.tensor_ru-Index__card')
        find_els = self.dr.get_elements_by('.tensor_ru-Index__card')
        if not find_els:
            return None
        for el in find_els:
            try:
                title = el.find_element(By.CSS_SELECTOR, '.tensor_ru-Index__card-title')
            except:
                continue
            if title.text == 'Сила в людях':
                return el, title
