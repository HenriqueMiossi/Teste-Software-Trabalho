from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from enum import Enum
import re

firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
geckodriver_path = r'C:\Windows\geckodriver.exe'

def set_values_on_inputs(driver, _start_value, _monthly_value, _interest_rate, _period):
    start_value = driver.find_element(By.ID, 'input-jc-valor-inicial')
    start_value.send_keys(f'{_start_value * 100}')

    monthly_value = driver.find_element(By.ID, 'input-jc-valor-mensal')
    monthly_value.send_keys(f'{_monthly_value * 100}')

    interest_rate = driver.find_element(By.ID, 'input-jc-taxa-juros')
    interest_rate.clear()
    interest_rate.send_keys(f'{_interest_rate}')

    period = driver.find_element(By.ID, 'input-jc-periodo')
    period.clear()
    period.send_keys(f'{_period}')

def click_calculate(driver):
    buttons = driver.find_elements(By.CLASS_NAME, 'btn-primary')
    calculate_button = [x for x in buttons if x.get_attribute('value') == 'Calcular'][0]
    calculate_button.click()

class Period(Enum):
    MONTH = 1
    YEAR = 2

def change_selection_values(driver, interest: Period, period: Period):
    interest_rate_selection = Select(driver.find_element(By.ID, 'input-jc-taxa-juros-frequencia'))
    if (interest == Period.YEAR):
        interest_rate_selection.select_by_value('anual')
    elif (interest == Period.MONTH):
        interest_rate_selection.select_by_value('mensal')
    else:
        raise TypeError('interest must be an instance of Period Enum')

    period_selection = Select(driver.find_element(By.ID, 'input-jc-periodo-unidade'))
    if (period == Period.YEAR):
        period_selection.select_by_value('ano(s)')
    elif (period == Period.MONTH):
        period_selection.select_by_value('mes(es)')
    else:
        raise TypeError('period must be an instance of Period Enum')

def sanitize_result(res):
    #re.search()
    res = re.sub("R\$ |\.", "", res)
    res = re.sub(",", ".", res)
    return float(res)

def get_result(driver):
    final_values = driver.find_elements(By.CLASS_NAME, 'h4')
    
    return {
        'final_value': sanitize_result(final_values[0].text),
        'initial_value': sanitize_result(final_values[1].text),
        'interest_rate': sanitize_result(final_values[2].text)
    }

def run_test(driver, start_value: float, monthly_value: float, interest_rate_value: int, interest_period: Period, period_value: int, period: Period):
    set_values_on_inputs(driver, start_value, monthly_value, interest_rate_value, period_value)
    change_selection_values(driver, interest_period, period)
    click_calculate(driver)

    driver.implicitly_wait(1.5)
    result = get_result(driver)
    
    print(result)

def main():
    options = Options()
    options.binary_location = firefox_path
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
    driver.get('https://investidorsardinha.r7.com/calculadoras/calculadora-de-juros-compostos/')

    run_test(driver, 100, 500, 6, Period.YEAR, 5, Period.YEAR)
    driver.refresh()
    run_test(driver, 100, 500, 6, Period.YEAR, 5, Period.MONTH)
    driver.refresh()
    run_test(driver, 100, 500, 6, Period.MONTH, 5, Period.YEAR)
    driver.refresh()
    run_test(driver, 100, 500, 6, Period.MONTH, 5, Period.MONTH)
    
    driver.close()

main()
