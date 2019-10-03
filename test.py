import time
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

states = [
    'AL', 'MO', 'AK', 'MT', 'AZ', 'NE', 'AR', 'NV', 'CA', 'NH', 
    'CO', 'NJ', 'CT', 'NM', 'DE', 'NY', 'NC', 'FL', 'ND', 'GA', 
    'OH', 'HI', 'OK', 'ID', 'OR', 'IL', 'PA', 'IN', 'RI', 'IA', 
    'SC', 'KS', 'SD', 'KY', 'TN', 'LA', 'TX', 'ME', 'UT', 'MD', 
    'VT', 'MA', 'VA', 'MI', 'WA', 'MN', 'WV', 'MS', 'WI', 'WY' 
    ]

items = ['zebra', 'lion', 'elephant', 'giraffe']



@pytest.mark.parametrize('state', states)
def test_correct_page(state):
    driver.get('https://jungle-socks.herokuapp.com/')
    if state == states[0]:
        time.sleep(2)
    else:
        time.sleep(.5)
    title = driver.title
    sub = driver.find_element_by_name('commit')
    zebra = driver.find_element_by_id('line_item_quantity_zebra').send_keys('1')
    select = Select(driver.find_element_by_name('state'))
    select.select_by_value(state)
    sub.click()
    time.sleep(.2)
    subtotal = driver.find_element_by_id('subtotal').text.strip('$')
    taxes = driver.find_element_by_id('taxes').text.strip('$')

    rate = float(taxes)/float(subtotal)
    rate = round(rate, 2)

    if state == 'NY':
        assert rate == 0.06
    elif state == 'CA':
        assert rate == 0.08
    elif state == 'MN':
        assert rate == 0.00
    else:
        assert rate == 0.05




@pytest.mark.parametrize('item', items)        
def test_prices(item):
    driver.get('https://jungle-socks.herokuapp.com/')
    if item == items[0]:
        time.sleep(2)
    else:
        time.sleep(.5)
    title = driver.title
    sub = driver.find_element_by_name('commit')

    if item == 'zebra':
        zebra = driver.find_element_by_id('line_item_quantity_zebra').send_keys('1')
    elif item == 'lion':
        lion = driver.find_element_by_id('line_item_quantity_lion').send_keys('1')
    elif item == 'elephant':
        elephant = driver.find_element_by_id('line_item_quantity_elephant').send_keys('1')
    elif item == 'giraffe':
        giraffe = driver.find_element_by_id('line_item_quantity_giraffe').send_keys('1')

    select = Select(driver.find_element_by_name('state'))
    select.select_by_value('NY')
    sub.click()
    time.sleep(.2)

    price = driver.find_element_by_id('subtotal').text.strip('$')
    price = float(price)

    if item == 'zebra':
        assert price == 13.00
    elif item == 'lion':
        assert price == 20.00
    elif item == 'elephant':
        assert price == 35.00
    elif item == 'giraffe':
        assert price == 17.00

    if item == items[-1]:
        driver.quit()