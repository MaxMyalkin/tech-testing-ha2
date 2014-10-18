# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def web_driver_wait_element(driver, selector):
    return WebDriverWait(driver, 30, 0.1).until(
        lambda d: d.find_element_by_css_selector(selector)
    )


def web_driver_wait_elements(driver, selector):
    return WebDriverWait(driver, 30, 0.1).until(
        lambda d: d.find_elements_by_css_selector(selector)
    )


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class BaseCampaignSettings(Component):
    CAMPAIGN_NAME = '.base-setting__campaign-name__input'
    PLAYGROUND = '#pad-mobile_app_web_service'
    ADVERTISING = '#product-type-6039'

    def __init__(self, driver):
        super(BaseCampaignSettings, self).__init__(driver)
        self.name = web_driver_wait_element(self.driver, self.CAMPAIGN_NAME)
        self.advertising = web_driver_wait_element(self.driver, self.ADVERTISING)

    def set_name(self, str):
        self.name.clear()
        self.name.send_keys(str)

    def set_playground(self):
        web_driver_wait_element(self.driver, self.PLAYGROUND).click()

    def set_advertising(self):
        self.advertising.click()


class AdsForm(Component):
    SAVE_BUTTON = '.banner-form__save-button'
    RESET_BUTTON = '.banner-form__reset'
    IMAGE = 'input[data-name="image"]'
    LINK = 'input[data-name="url"]'
    TITLE = 'input[data-name="title"]'
    TEXT = 'textarea[data-name="text"]'

    @property
    def added_banner(self):
        return BannerPreview(self.driver)

    def set_title(self, title):
        self.title.send_keys(title)

    def set_text(self, text):
        self.text.send_keys(text)

    def set_image(self, path):
        web_driver_wait_element(self.driver, self.IMAGE).send_keys(path)

    def set_link(self, link):
        self.link.send_keys(link)

    @property
    def link(self):
        inputs = web_driver_wait_elements(self.driver, self.LINK)
        for element in inputs:
            if element.is_displayed():
                return element

    @property
    def title(self):
        return web_driver_wait_element(self.driver, self.TITLE)

    @property
    def text(self):
        return web_driver_wait_element(self.driver, self.TEXT)

    def submit(self):
        return self.driver.find_element_by_css_selector(self.SAVE_BUTTON).click()

    def reset(self):
        web_driver_wait_element(self.driver, self.RESET_BUTTON).click()

    def loading_image(self, driver):
        images = driver.find_elements_by_css_selector('.banner-preview .banner-preview__img')
        for image in images:
            if image.value_of_css_property("width") == '90px':
                return WebDriverWait(image, 30, 0.1).until(
                    lambda d: d.value_of_css_property("background-image") is not None)

    def wait_picture(self):
        WebDriverWait(self.driver, 30, 0.1).until(lambda d: self.loading_image(d))


class Settings(Component):
    WHOM = '[data-name="whom"]'
    ALL_SETTINGS = '.all-settings'
    SETTINGS_BODY = '.all-settings__body'

    def wait_for_settings(self):
        web_driver_wait_elements(self.driver, self.WHOM)
        web_driver_wait_elements(self.driver, self.ALL_SETTINGS)
        web_driver_wait_elements(self.driver, self.SETTINGS_BODY)

    @property
    def age(self):
        self.wait_for_settings()
        return Slider(driver=self.driver)

    @property
    def income(self):
        self.wait_for_settings()
        return Income(driver=self.driver)


class Slider(Component):
    LEFT_SLIDER = '.range-slider__handle.range-slider__handle_left'
    RIGHT_SLIDER = '.range-slider__handle.range-slider__handle_right'
    AGE = '[data-name="age"] .campaign-setting__value.js-setting-value'

    def toggle(self):
        self.element.click()
        if self.left_slider.is_displayed():
            WebDriverWait(self.driver, 30, 0.1).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.LEFT_SLIDER)))
        else:
            WebDriverWait(self.driver, 30, 0.1).until(
                expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, self.LEFT_SLIDER)))

    @property
    def left_slider(self):
        return web_driver_wait_element(self.driver, self.LEFT_SLIDER)

    @property
    def right_slider(self):
        return web_driver_wait_element(self.driver, self.RIGHT_SLIDER)

    @property
    def element(self):
        web_driver_wait_element(self.driver, '[data-name="age"]')
        return WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.AGE)))

    def get_range(self):
        left = self.left_slider.text
        right = self.right_slider.text
        return left, right

    def move_left_slider(self, offset):
        action_chain = ActionChains(self.driver)
        action_chain.drag_and_drop_by_offset(self.left_slider, offset, 0).perform()

    def move_right_slider(self, offset):
        action_chain = ActionChains(self.driver)
        action_chain.drag_and_drop_by_offset(web_driver_wait_element(self.driver, self.RIGHT_SLIDER), offset,
                                             0).perform()

    def get_text(self):
        return self.element.text


class Income(Component):
    GREATER = '#income_group-9288'
    MIDDLE = '#income_group-9287'
    LESS = '#income_group-9286'
    INCOME = '[data-name="income_group"] .campaign-setting__value.js-setting-value'

    @property
    def greater(self):
        return web_driver_wait_element(self.driver, self.GREATER)

    @property
    def middle(self):
        return web_driver_wait_element(self.driver, self.MIDDLE)

    @property
    def less(self):
        return web_driver_wait_element(self.driver, self.LESS)

    @property
    def element(self):
        web_driver_wait_element(self.driver, '[data-name="income_group"]')
        return WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.INCOME)))

    def toggle(self):
        self.element.click()
        if self.greater.is_displayed():
            WebDriverWait(self.driver, 30, 0.1).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.GREATER)))
        else:
            WebDriverWait(self.driver, 30, 0.1).until(
                expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, self.GREATER)))

    def get_checked(self):
        return self.less.is_selected(), self.middle.is_selected(), self.greater.is_selected()

    def get_text(self):
        return self.element.text


class Projection(Component):
    AGE = '.projection .projection__age-targeting__text'

    @property
    def age(self):
        return web_driver_wait_element(self.driver, self.AGE)


class BannerPreview(Component):
    TITLE = '.added-banner .banner-preview__title'
    IMAGE = '.added-banner .banner-preview__img'
    TEXT = '.added-banner .banner-preview__text'

    @property
    def title(self):
        return web_driver_wait_element(self.driver, self.TITLE)

    @property
    def text(self):
        return web_driver_wait_element(self.driver, self.TEXT)

    @property
    def image(self):
        images = web_driver_wait_elements(self.driver, self.IMAGE)
        for image in images:
            if image.value_of_css_property('background-image') is not None:
                return image

    def get_info(self):
        return self.title.text, self.text.text, self.image.value_of_css_property('background-image')