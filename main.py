from http import client
from optparse import Values
import lxml
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


base_url = "http://192.168.0.1"


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

def get_page(url):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    password = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, 'password')))
    password.send_keys('mzyfqtg@')

    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(1)

    get_values(driver.page_source)
    driver.close()


get_page(base_url)
