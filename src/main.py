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
start_value.send_keys('600000') # R$6000,00

monthly_value = driver.find_element(By.ID, 'input-jc-valor-mensal')
monthly_value.send_keys('50000') # R$500,00

interest_rate = driver.find_element(By.ID, 'input-jc-taxa-juros')
interest_rate.clear_field()
interest_rate.send_keys('9')

period = driver.find_element(By.ID, 'input-jc-periodo')
period.clear_field()
period.send_keys('1')
