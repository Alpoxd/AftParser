from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup

clear = lambda: os.system('cls')

clear()

link = "https://www.aeroflot.ru/sb/app/ru-ru#/search?adults="
vzr = input("Adults (12+): ")
det = input("Children: ")
_from = input("From: ")
_to = input("To: ")
date = input("Date (YYYYDDMM): ")
link += vzr + "&cabin=economy&children=" + det + "&infants=0&routes=" + _from + "." + date + "." + _to

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.minimize_window()

driver.get(link)

clear()
print("Loading Data.")
delay = 20

try:
    element = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button.button--wide.button--lg")))
finally:
    driver.find_element(By.CLASS_NAME, "button.button--wide.button--lg").click()
    
clear()
print("Loading Data..")

try:
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "flight-search")))
finally:
    clear()
    print("Calculating...")
soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()
clear()

results = []
datas = soup.find_all('div', class_='flight-search__inner')
for data in datas:
    from_ = data.find('div', class_='time-destination__from')
    to_ = data.find('div', class_='time-destination__to')
    
    tmp = from_.find('span', class_='time-destination__time')
    if (tmp != None):
        s = tmp.text
    tmp = from_.find('span', class_='time-destination__airport')
    if (tmp != None):
        s += ' ' + tmp.text
    tmp = from_.find('span', class_='time-destination__terminal')
    if (tmp != None):
        s += ' ' + tmp.text + ' - '
    else:
        s += ' - '
    
    tmp = to_.find('div', class_='time-destination__time')
    if (tmp != None):
        tmp1 = tmp.find('span')
        s += tmp1.text
        tmp2 = tmp.find('span', class_='time-destination__plusday')
        if (tmp2 != None):
            s += ' ' + tmp2.text
    tmp = to_.find('span', class_='time-destination__airport')
    if (tmp != None):
        s += ' ' + tmp.text
    tmp = to_.find('span', class_='time-destination__terminal')
    if (tmp != None):
        s += ' ' + tmp.text
    
    
    tmp = data.find('div', class_='flight-search__company-name')
    if (tmp != None):
        s += ' ' + tmp.text
    tmp = data.find('div', class_='flight-search__plane-number')
    if (tmp != None):
        s += ' ' + tmp.text
    tmp = data.find('div', class_='flight-search__plane-model h-text--break')
    if (tmp != None):
        s += ' (' + tmp.text + ')'
    tmp = data.find('div', class_='flight-search__time')
    if (tmp != None):
        s += ' ' + tmp.text
    tmp = data.find('div', class_='flight-search__price-text')
    if (tmp != None):
        s += ' ' + tmp.text
        s = s[:-1]
        s += 'RUB'
    tmp = data.find('div', class_='flight-search__left')
    if (tmp != None):
        s += ' ' + tmp.text
    results.append(s)
for data in results:
    print(data)
datetxt = date + ".txt"
_wr = input("If you want to save to " + datetxt + ", type w: ")
if (_wr == "w"):
    with open(datetxt, "w") as output:
        output.write("From-To: ")
        output.write(_from)
        output.write(_to)
        output.write("\n")
        for data in results:
            output.write(data)
            output.write("\n")
    print("Saved to " + datetxt)
exit()