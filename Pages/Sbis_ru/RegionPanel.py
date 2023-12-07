from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from Constants import ELEMENT_WAIT_TIMEOUT
from Pages.Base import Base


class RegionPanel(Base):

    def init_page_elements(self):
        # Ожидаем появления самой панели
        wait = WebDriverWait(self.dr_helper.get_driver(), timeout=ELEMENT_WAIT_TIMEOUT)
        self.panel = wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, '.sbis_ru-Region-Panel'))
        # Инициализируем элементы панели
        self.region_list = self.dr_helper.get_element_by_css('.sbis_ru-Region-Panel__list')
        self.region_items = self.dr_helper.get_elements_by_css('.sbis_ru-Region-Panel__item')

    def select_region(self, region):
        region_caption = None
        if not region:
            return Exception('Не указан параметр region')
        if not self.region_items:
            return Exception('Отсутствуют регионы в списке')
        for region_item in self.region_items:
            region_caption_el = region_item.find_element(By.TAG_NAME, 'span')
            if region_caption_el:
                region_caption = region_caption_el.text
            if region_caption == region:
                region_item.click()
                break
