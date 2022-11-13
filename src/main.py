from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
geckodriver_path = r'C:\Windows\geckodriver.exe'

options = Options()
options.binary_location = firefox_path
driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)

driver.get('https://investidorsardinha.r7.com/calculadoras/calculadora-de-juros-compostos/')

start_value = driver.find_element(By.ID, 'input-jc-valor-inicial')
start_value.send_keys('100000') # R$1000,00

monthly_value = driver.find_element(By.ID, 'input-jc-valor-mensal')
monthly_value.send_keys('0') # R$0,00

interest_rate = driver.find_element(By.ID, 'input-jc-taxa-juros')
interest_rate.clear()
interest_rate.send_keys('6')

period = driver.find_element(By.ID, 'input-jc-periodo')
period.clear()
period.send_keys('4')

buttons = driver.find_elements(By.CLASS_NAME, 'btn-primary')
calculate_button = [x for x in buttons if x.get_attribute('value') == 'Calcular'][0]
calculate_button.click()


def blabla(x, y)