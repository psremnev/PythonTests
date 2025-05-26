from selenium.webdriver.common.by import By
from pages.Base import Base


class ContactsPopup(Base):

    def init_page_elements(self):
        self.go_to_contacts_btn = self.dr.get_element_by('//a[@href="/contacts"]', By.XPATH)
