from compoundinterest import CompoundInterest
import re
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from enum import Enum

# firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# geckodriver_path = r'C:\Windows\geckodriver.exe'

# options = Options()
# options.binary_location = firefox_path
# driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
driver = webdriver.Chrome()
url = "https://investidorsardinha.r7.com/calculadoras/calculadora-de-juros-compostos/"
result = {"final_value": -1, "initial_value": -1, "interest_rate": -1}
compound_interest = CompoundInterest(1000, 6, 4)

# Is there a better way to do this?
# How does | works?
def sanitize_result(res):
    #re.search()
    res = re.sub("R\$ |\.", "", res)
    res = re.sub(",", ".", res)
    return float(res)

# driver.implicity_wait(0.5)
def get_result():
    driver.implicitly_wait(1.5)

    results = driver.find_elements(By.CSS_SELECTOR, "#calculation-result .p-3")

    for res in results:
        label = res.find_element(By.TAG_NAME, "p")
        content = res.find_element(By.TAG_NAME, "div")
        if label.text == "Valor total final":
            result["final_value"] = sanitize_result(content.text)
        elif label.text == "Valor total investido":
            result["initial_value"] = sanitize_result(content.text)
        elif label.text == "Total em juros":
            result["interest_rate"] = sanitize_result(content.text)
        else:
            print("Fail.")

def run_test(compound_interest):
    driver.get(url)

    initial_value = driver.find_element(By.ID, 'input-jc-valor-inicial')
    monthly_contribution = driver.find_element(By.ID, 'input-jc-valor-mensal')
    interest_rate = driver.find_element(By.ID, 'input-jc-taxa-juros')
    period = driver.find_element(By.ID, 'input-jc-periodo')
    buttons = driver.find_elements(By.CLASS_NAME, 'btn')
    calc = [btn for btn in buttons if btn.get_attribute('value') == 'Calcular'][0]

    initial_value.clear()
    monthly_contribution.clear()
    interest_rate.clear()
    period.clear()
    initial_value.send_keys(compound_interest.p * 100)
    interest_rate.send_keys(compound_interest.r)
    period.send_keys(compound_interest.t)
    calc.click()
    get_result()
    driver.close()

# class Period(Enum):
#     MONTH = 1
#     YEAR = 2

# def change_selection_values(interest: Period, period: Period):
#     interest_rate_selection = Select(driver.find_element(By.ID, 'input-jc-taxa-juros-frequencia'))
#     if (interest == Period.YEAR):
#         interest_rate_selection.select_by_value('anual')
#     elif (interest == Period.MONTH):
#         interest_rate_selection.select_by_value('mensal')
#     else:
#         raise TypeError('interest must be an instance of Period Enum')

#     period_selection = Select(driver.find_element(By.ID, 'input-jc-periodo-unidade'))
#     if (period == Period.YEAR):
#         period_selection.select_by_value('ano(s)')
#     elif (period == Period.MONTH):
#         period_selection.select_by_value('mes(es)')
#     else:
#         raise TypeError('period must be an instance of Period Enum')

# change_selection_values(Period.MONTH, Period.MONTH)
