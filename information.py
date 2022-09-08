from socket import timeout
import time
import serial
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

from bs4 import BeautifulSoup

base_url = "http://192.168.0.1"
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

def get_values(html):

    soup = BeautifulSoup(html, "lxml")

    header = soup.find("div", {"id": "header"})
    top_layout = header.find("div", {"id": "top_layout"})
    div = top_layout.find("div", {"class", "container"})
    ul = div.find("ul", {"id": "top_icon_layout"})
    info_lists = ul.find_all("li")

    find_signal = info_lists[0].find("a").find("i")
    signal_strength = find_signal['class']
    client_count = info_lists[4]['title']
    battery = info_lists[-1]['title']

    values = {"signal_strength": signal_strength,
              "client_count": client_count, "battery": battery
              }

    return values

def get_page(url):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    password = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, 'password')))
    password.send_keys('mzyfqtg@')

    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(1)

    page_source = driver.page_source
    driver.close()

    return page_source

def charge():
    ser.writelines(b'1') 

def stop_charge():
    ser.writelines(b'0')
    time.sleep(200)

while True:

    page_source = get_page(base_url)
    values = get_values(page_source)
    signal_strength = values['signal_strength'][0][15:]
    client_count = values['client_count'][14:]
    battery = values['battery'][0]

    try:
        if int(battery) < 20:
            charge() 
        else:
            stop_charge()

    except Exception as e:
        print(e)



