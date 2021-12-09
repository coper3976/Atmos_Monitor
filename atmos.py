from selenium import webdriver
import sys, os
from bs4 import BeautifulSoup, element
import pyperclip
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
from pathos.multiprocessing import ProcessingPool as Pool
from discord_hooks import Webhook
from tqdm import tqdm


# 크롬이 있는 폴더로 이동..
#cd C:\Program Files (x86)\Google\Chrome\Application

# 크롬 디버깅 창 띄우기
#chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"

# 디버깅 크롬창이 떠 있는지 확인
#netstat -ano | findstr 9222

#pyinstaller -F --add-binary "C:\Users\user\Desktop\chromedriver\chromedriver.exe;." tt.py

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/93.0.4577.82 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
options.add_argument("--start-maximized") 
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(r'./chromedriver', options=options)

driver.get('http://www.atmos-seoul.com/shop/shopbrand.html?xcode=003&type=N&mcode=001&gf_ref=Yz12UEthNk0=')
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

divs = soup.find('div', class_='item-wrap prd-parts')
divss = divs.find_all('dl', class_='item-list')

for div in divss:
    brand = div.find('li', class_='list-brand-name').text.strip()
    ProductID = div.find('li', class_='prd-name').text.strip()
    price = div.find('li', class_='prd-price').text.strip()
    productLink = "http://www.atmos-seoul.com" + div.find('a', class_='')['href'].strip()
    img = "http://www.atmos-seoul.com" + div.find('dt', class_='thumb').img['src']


if __name__ == "__main__":
    ''' --------------------------------- Main --------------------------------- '''
    MONITOR_DELAY = 5
    # 기존 상품정보 가져오기
    print("DB 생성중...")
    driver.get('http://www.atmos-seoul.com/shop/shopbrand.html?xcode=003&type=N&mcode=001&gf_ref=Yz12UEthNk0=')
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find('div', class_='item-wrap prd-parts')
    divss = divs.find_all('dl', class_='item-list')

    product_db = dict()
    for div in divss:
        brand = div.find('li', class_='list-brand-name').text.strip()
        ProductID = div.find('li', class_='prd-name').text.strip()
        price = div.find('li', class_='prd-price').text.strip()
        productLink = "http://www.atmos-seoul.com" + div.find('a', class_='')['href'].strip()
        img = "http://www.atmos-seoul.com" + div.find('dt', class_='thumb').img['src']
        product_db[ProductID] = [brand, ProductID, price, productLink, img] 

    #테스트
    product_db.pop('AT X NE X HAT BLACK')

    #모니터링 시작
    print("<모니터링 시작>")
    for loopCnt in tqdm(range(int(5))):
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        print("모니터링 중..")
        driver.get('http://www.atmos-seoul.com/shop/shopbrand.html?xcode=003&type=N&mcode=001&gf_ref=Yz12UEthNk0=')

        divs = soup.find('div', class_='item-wrap prd-parts')
        divss = divs.find_all('dl', class_='item-list')
        for div in divss:
            brand = div.find('li', class_='list-brand-name').text.strip()
            ProductID = div.find('li', class_='prd-name').text.strip()
            price = div.find('li', class_='prd-price').text.strip()
            productLink = "http://www.atmos-seoul.com" + div.find('a', class_='')['href'].strip()
            img = "http://www.atmos-seoul.com" + div.find('dt', class_='thumb').img['src']
            if ProductID not in product_db.keys():
                product_db[ProductID] = [brand, ProductID, price, productLink, img]
                print("새 상품이 추가 됐습니다.")
                print("브랜드 :", brand)
                print("제품명 :", ProductID)
                print("가격 :", price)
                print("제품링크 :", productLink)
                print("제품 이미지 :", img)
        time.sleep(MONITOR_DELAY)








