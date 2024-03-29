﻿from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

from common.logger import set_logger
from config.const import *
logger = set_logger(__name__)

class Driver():
    
    def __init__(self, headless_flg:bool=False):
        self.headless_flg = headless_flg
        self.driver = self.set_driver()
        
    def set_driver(self):
        # Chromeドライバーの読み込み
        options = ChromeOptions()

        # ヘッドレスモードの設定
        if self.headless_flg:
            options.add_argument('--headless')
        

        logger.info(f"headless:{self.headless_flg} ")
        
        options.add_argument('--user-agent=' + HEADER.USER_AGENT)
        #self.options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')          # シークレットモードの設定を付与
        options.add_argument('disable-infobars') # AmazonLinux用
        
        # ChromeのWebDriverオブジェクトを作成する。
        try:
            driver = Chrome(ChromeDriverManager().install(), options=options)
            # driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
            #                           options=options)
            logger.info("chrome driver起動成功")
            return driver
        except Exception as e:
            logger.error(f"driver起動エラー:{e}")
            return None
        
    def wait_for_element(self, element_name:str, element_kind:str, wait_limit=100):
        wait = WebDriverWait(self.driver, wait_limit)  # 指定要素が表示されるまで待つ
        if element_kind == "ID":
            by=By.ID
        elif element_kind == "CSS_SELECTOR":
            by=By.CSS_SELECTOR
        elif element_kind == "CSS_NAME":
            by=By.CLASS_NAME
        elif element_kind == "NAME":
            by=By.NAME
        else:
            by=By.CSS_SELECTOR
        wait.until(expected_conditions.visibility_of_element_located(
            (by, element_name)))
    
    def select_element_by_name(self,name:str,select_text:str,mode:str="",by:str="NAME"):
        if by == "NAME":
            select_element = self.driver.find_element_by_name(name)
        elif by == "ID":
            select_element = self.driver.find_element_by_id(name)
        else:
            select_element = self.driver.find_element_by_css_selector(name)
        select_object = Select(select_element)
        # Select an <option> based upon its text
        if mode=="VALUE":
            select_object.select_by_value(select_text)
        else:
            select_object.select_by_visible_text(select_text)
        return select_object.first_selected_option
    
    def click_element_by_css_selector(self,selector):
        elms=self.driver.find_elements_by_css_selector(selector)
        if len(elms)>=1:
            elms[0].click()
            return True
        return False
    
    def get_text_element_by_css_selector(self,selector):
        elms=self.driver.find_elements_by_css_selector(selector)
        if len(elms)>=1:
            return elms[0].text
        return ""
    
    def quit(self):
        self.driver.quit()
        
    def __del__(self):
        self.quit()