import urlparse

from selenium.webdriver.support.wait import WebDriverWait

from tests.page_objects.components import AuthForm, TopMenu

from tests.page_objects.components import Settings, BaseCampaignSettings, AdsForm, Projection


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'
    CREATE = '.main-button-new'

    @property
    def projection(self):
        return Projection(self.driver)

    @property
    def base_settings(self):
        return BaseCampaignSettings(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def ads_form(self):
        return AdsForm(self.driver)

    @property
    def settings(self):
        return Settings(self.driver)

    @property
    def create_btn(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CREATE)
        )


class CampaignsPage(Page):
    PATH = '/ads/campaigns/'
    LAST_EDIT = '.campaign-row .control__link_edit'

    @property
    def edit_last(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.LAST_EDIT)
        )