import time

from selenium import webdriver


url = 'https://login.taobao.com/member/login.jhtml'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches',
                                ['enable-automation'])

driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
driver.maximize_window()
time.sleep(2)
driver.find_element_by_class_name('ph-label').send_keys('18520968024')
driver.find_element_by_class_name('login-text').send_keys('sunbiao931024wd')
driver.find_element_by_class_name('J_Submit').click()
time.sleep(2)
driver.close()