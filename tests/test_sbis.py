import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from constants import ELEMENT_WAIT_TIMEOUT
from pages.sbis_ru.Home import Home as SbisHome
from pages.tensor_ru.Home import Home as TensorHome
from pages.tensor_ru.About import About as TensorAbout
from pages.sbis_ru.Contacts import Contacts
from driver import Driver
from pages.sbis_ru.RegionPanel import RegionPanel
from pages.sbis_ru.Download import Download
from pages.sbis_ru.ContactsPopup import ContactsPopup


class TestCase:

    def setup_class(self):
        self.dr = Driver()
        self.page_sbis = SbisHome(self.dr)
        self.page_tensor = TensorHome(self.dr)
        self.page_tensor_about = TensorAbout(self.dr)
        self.page_contacts = Contacts(self.dr)
        self.page_download = Download(self.dr)
        self.contacts_popup = ContactsPopup(self.dr)

    def teardown_class(self):
        self.dr.quit()

    def test_check_elements(self):
        self.page_sbis.open()
        self.page_sbis.contacts_popup_btn.click()
        self.contacts_popup.init_page_elements()
        self.contacts_popup.go_to_contacts_btn.click()

        # Переход на сайт tensor.ru по баннеру
        self.page_contacts.init_page_elements()
        self.page_contacts.banner.click()
        windows = self.dr.get_windows()
        assert len(windows) > 1, 'Не открылась новая вкладка'

        # Закроем текущую вклдаку и перейдем на новую вкладку
        window_tensor = self.dr.get_windows()[1]
        self.dr.close_window()
        self.dr.switch_to_window(window_tensor)

        # Проверим наличие блока "Сила в людях"
        self.page_tensor.init_page_elements()
        assert self.page_tensor.power_in_people_card_title_is_visible(), 'Блок "Сила в людях" не отображается'

        # Переходим в карточке "Сила в людях" по кнопке "Подробнее" и проверяем правильный url адреса страницы
        self.page_tensor.power_in_people_card_more.click()
        assert self.dr.get_current_url() == 'https://tensor.ru/about', ('Адрес страницы не соот.'
                                                                               ' "https://tensor.ru/about"')

        # Проверим что все картинки в блоке "Работаем одного размера"
        self.page_tensor_about.init_page_elements()
        assert self.page_tensor_about.work_section_images_has_correct_size(), ('Картинки в блоке "Работаем"'
                                                                               ' имеют разный размер')

    def test_change_region(self):
        region_name = 'Ярославская обл.'
        region_partner_list = 'Ярославль'
        select_region = '37 Ивановская обл.'
        select_region_name_url = '37-ivanovskaya-oblast'
        select_region_partner_list = 'Иваново'

        # Проверим текущий регион
        self.page_contacts.open()
        assert self.page_contacts.current_region.text == region_name

        # Проверим отображение списков партнера по городу
        assert (self.dr.el_is_displayed(self.page_contacts.city_list)
                and self.dr.el_is_displayed(self.page_contacts.partners_city_list)), \
            'Список партнеров по городу не отображается'
        assert self.page_contacts.has_city_in_partners_list(region_partner_list), \
            'В списке патнеров не отображается верный регион'

        # Выбор региона и проверка
        self.page_contacts.current_region.click()
        regionPanel = RegionPanel(self.dr)
        regionPanel.init_page_elements()
        regionPanel.select_region(select_region)

        # Подождем смены региона
        wait = WebDriverWait(self.dr.get_driver(), timeout=ELEMENT_WAIT_TIMEOUT)
        wait.until(lambda d: self.page_contacts.current_region.text != region_name)

        assert self.dr.get_current_url().find(select_region_name_url) > -1, \
            'Не изменился url страницы после выбора нового региона'
        assert self.dr.get_driver().title == 'Saby Контакты — Ивановская область', \
            'Не изменился заголовок после выбора нового региона'
        assert self.page_contacts.has_city_in_partners_list(select_region_partner_list), \
            'В списке патнеров не отображается верный регион'

    def test_download_sbis_plugin(self):
        # Открываем страницу сбис ру и нажимаем скачать сбис плагин
        self.page_sbis.open()
        self.page_sbis.download_btn.click()

        # Переходим на нужный таб для скачивания файла
        self.page_download.init_page_elements()
        # тут странное поведение страницы, она обновляется 2 раза, поэтому пока так
        time.sleep(1)
        self.page_download.plugin_tab.click()
        tab_by_os = self.page_download.get_tab_by_platform()
        tab_by_os.click()

        # Находим ссылку на файл и размер файла в тексте если он есть
        link_el = self.page_download.find_first_link_for_download()
        link = link_el.get_attribute('href')
        size_from_text_arr = re.findall(r'\d+', link_el.text)
        if size_from_text_arr:
            size_from_text = '.'.join(size_from_text_arr)

        # Скачиваем файл, извлекаем нужные данные
        content, download_file_size = self.page_download.download_file_by_link(link)

        # Сохраняем файл
        self.page_download.save_file(content)

        # Так как для линукса нету размера
        if bool(size_from_text):
            assert size_from_text == download_file_size, \
                'Не совпадает размер скачанного файла и размер указанный на сайте'
