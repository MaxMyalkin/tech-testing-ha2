# coding=utf-8
import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.wait import WebDriverWait

from tests.page_objects.components import BannerPreview
from tests.page_objects.pages import CreatePage, CampaignsPage, AuthPage


def hide_menu(driver):
    driver.execute_script(""" $('.head').hide(); """)
    # WebDriverWait(driver, 30, 0.1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#portal-menu__toolbar')))


def loading_image(driver):
    images = driver.find_elements_by_css_selector('.banner-preview .banner-preview__img')
    for image in images:
        if image.value_of_css_property("width") == '90px':
            return WebDriverWait(image, 30, 0.1).until(
                lambda d: d.value_of_css_property("background-image") is not None)


def login(driver):
    auth_page = AuthPage(driver)
    auth_page.open()
    auth_form = auth_page.form
    auth_form.set_domain(Constants.DOMAIN)
    auth_form.set_login(Constants.USERNAME)
    auth_form.set_password(Constants.PASSWORD)
    auth_form.submit()


class Constants:
    APP = 'https://play.google.com/store/apps/details?id=com.google.android.gm'
    IMG_PATH = os.path.abspath('static/img.jpg')
    TITLE = "title"
    TEXT = "text"
    USERNAME = 'tech-testing-ha2-23@bk.ru'
    PASSWORD = os.environ['TTHA2PASSWORD']
    DOMAIN = '@bk.ru'


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        login(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        email = create_page.top_menu.get_email()
        self.assertEqual(Constants.USERNAME, email)

    def test_income_selected(self):
        text_unselected = u'Не учитывать'
        text_selected = u'Выбран'
        create_page = CreatePage(self.driver)
        create_page.open()

        settings = create_page.settings
        income = settings.income
        hide_menu(self.driver)
        self.assertEqual(text_unselected, income.get_text(), "Неправильный текст в блоке с доходом")
        income.toggle()
        income.greater.click()
        self.assertEqual(text_selected, income.get_text(), "Неправильный текст в блоке с доходом")
        income.greater.click()
        self.assertEqual(text_unselected, income.get_text(), "Неправильный текст в блоке с доходом")

    def test_saving_ages_after_hiding(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        slider = create_page.settings.age
        slider.toggle()
        hide_menu(self.driver)

        slider.move_left_slider(100)
        slider.move_right_slider(-100)

        left, right = slider.get_range()

        slider.toggle()
        slider.toggle()

        self.assertEqual((left, right), slider.get_range(), "Значения после скрытия не совпадают")

    def test_saving_income_after_hiding(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        income = create_page.settings.income
        income.toggle()
        hide_menu(self.driver)

        income.less.click()
        income.greater.click()
        income.toggle()
        income.toggle()
        self.assertEqual((True, False, True), income.get_checked(), "Значения после скрытия не совпадают")

    def test_ads_add(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        settings = create_page.base_settings
        settings.set_advertising()
        settings.set_playground()
        settings.set_name("OH MY NAME")
        ads_form = create_page.ads_form
        ads_form.set_link(Constants.APP)
        ads_form.set_title(Constants.TITLE)
        ads_form.set_text(Constants.TEXT)
        ads_form.set_image(Constants.IMG_PATH)
        WebDriverWait(self.driver, 30, 0.1).until(lambda d: loading_image(d))
        ads_form.submit()

        banner = ads_form.added_banner
        self.assertEqual(Constants.TITLE, banner.title.text, "созданный баннер не совпадает с заполненным")
        self.assertEqual(Constants.TEXT, banner.text.text, "созданный баннер не совпадает с заполненным")
        self.assertIsNotNone(banner.image.value_of_css_property('background-image'), "Картинка не добавилась")

    def test_slider(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        settings = create_page.settings
        slider = settings.age
        slider.toggle()
        hide_menu(self.driver)

        assert slider.left_slider.text not in slider.get_text() and slider.right_slider.text not in slider.get_text()
        slider.move_left_slider(100)
        assert slider.left_slider.text in slider.get_text() and slider.right_slider.text not in slider.get_text()
        slider.move_right_slider(-100)
        assert slider.left_slider.text in slider.get_text() and slider.right_slider.text in slider.get_text()
        slider.move_left_slider(-100)
        assert slider.left_slider.text not in slider.get_text() and slider.right_slider.text in slider.get_text()

    def test_projection_age_text(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        settings = create_page.settings
        slider = settings.age
        slider.toggle()
        hide_menu(self.driver)
        slider.move_left_slider(100)
        projection = create_page.projection
        assert slider.get_text() == projection.age.text

    def test_publish_campaign(self):
        campaign_name = "NAME THE COMPANY PLEASE"

        create_page = CreatePage(self.driver)
        create_page.open()
        settings = create_page.base_settings
        settings.set_advertising()
        settings.set_playground()
        settings.set_name(campaign_name)
        ads_form = create_page.ads_form
        ads_form.set_link(Constants.APP)
        ads_form.set_title(Constants.TITLE)
        ads_form.set_text(Constants.TEXT)
        ads_form.set_image(Constants.IMG_PATH)
        WebDriverWait(self.driver, 30, 0.1).until(lambda d: loading_image(d))
        ads_form.submit()

        banner = BannerPreview(self.driver)
        banner_info = banner.get_info()

        settings = create_page.settings
        income = settings.income
        income.toggle()
        income.less.click()
        income.middle.click()
        income_info = income.get_checked()

        create_page.create_btn.click()

        campaign_pages = CampaignsPage(self.driver)
        campaign_pages.edit_last.click()
        banner_info_new = banner.get_info()
        income_info_new = income.get_checked()
        self.assertEqual(banner_info, banner.get_info(), "Значения в редактировании не совпадают с исходными")
        self.assertEqual(income_info, income.get_checked(), "Значения в редактировании не совпадают с исходными")






