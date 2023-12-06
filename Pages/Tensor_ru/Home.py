from selenium.webdriver.common.by import By

class Home:
    url = 'https://tensor.ru/'

    def __init__(self, dr_helper):
        self.dr_helper = dr_helper

    def open(self):
        self.dr_helper.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        self.power_in_people_card, self.power_in_people_card_title = self.find_power_in_people_card()
        self.power_in_people_card_more = self.power_in_people_card.find_element(By.LINK_TEXT, 'Подробнее')

    def power_in_people_card_title_is_visible(self):
        return self.power_in_people_card_title.is_displayed() and self.power_in_people_card_title.text == 'Сила в людях'
    def find_power_in_people_card(self):
        find_els = self.dr_helper.get_elements_by_css('.tensor_ru-Index__card')
        if not find_els:
            return None
        for el in find_els:
            try:
                title = el.find_element(By.CSS_SELECTOR, '.tensor_ru-Index__card-title')
            except:
                continue
            if title.text == 'Сила в людях':
                return el, title
