from selenium.webdriver.common.by import By
from pages.Base import Base


class About(Base):
    url = 'https://tensor.ru/about'

    def open(self):
        self.dr.open(self.url)
        self.init_page_elements()

    def init_page_elements(self):
        self.work_section, self.work_section_title = self.find_work_section()
        self.work_section_images = self.work_section.find_elements(By.TAG_NAME, 'img')

    def find_work_section(self):
        find_els = self.dr.get_elements_by('.tensor_ru-section')
        if not find_els:
            return None
        for el in find_els:
            try:
                title = el.find_element(By.CSS_SELECTOR, '.tensor_ru-About__block-title')
            except:
                continue
            if title.text == 'Работаем':
                return el, title

    def work_section_images_has_correct_size(self):
        check_height = None
        check_width = None
        status = True
        if not self.work_section_images:
            return Exception('work_section_images is None')
        for img in self.work_section_images:
            rect = img.rect
            height = rect.get('height')
            width = rect.get('width')
            if not check_width and not check_height:
                check_width = width
                check_height = height
                continue
            if height != check_height and width != check_width:
                status = False
                break
        return status
