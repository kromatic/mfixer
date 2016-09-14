#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_fact():
    driver.get('http://facts.randomhistory.com/')
    return driver.find_element_by_class_name('home-text').text

driver = webdriver.Firefox()
while 1:
    print('\n' + get_fact() + '\n')
    again = input('Get another fact? (Y/n) ')
    if again.strip().lower() == 'n':
        break
driver.quit()
