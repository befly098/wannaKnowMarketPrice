#-*- coding: UTF-8 -*-
#!/usr/bin/env python

# we may not use bs4 and requests...
import time
from imp import reload
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
import pymysql
import chardet
import bigram

# Function that scrap product information at "NAVER Shopping"
def SSG_crawling(browser, market_data):

    site_title = "SSG"

    for page_num in range(5):
        browser.get("http://www.ssg.com/search.ssg?target=all&query=%EB%8B%8C%ED%85%90%EB%8F%84%20%EC%8A%A4%EC%9C%84%EC%B9%98&page="+str(page_num + 1))
        # [todo] add loading command

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        element_list = browser.find_elements_by_xpath("//ul/li/div[@class='cunit_info']")

        # print product information while iterating parent elements
        for element in element_list:
            # product price has two types of tag at NAVER Shopping
            # so, we have to check two tags
            
            product_title = element.find_element_by_xpath("./div[2]/div[1]/a/em[1]").text.encode("utf-8")
            product_price = element.find_element_by_xpath("./div[3]/div[1]/em[1]").text.encode("utf-8")

            print product_title, product_price

            scrap_time = time.strftime('%Y-%m-%d %H:%M:%S')
            market_data.append([site_title, product_title, product_price, scrap_time])

    print ("[INFO] SSG crawl succeeded")
    return market_data

def InterPark_crawling(browser, market_data):

    site_title = "InterPark"

    browser.get("http://isearch.interpark.com/isearch?q=%EB%8B%8C%ED%85%90%EB%8F%84%20%EC%8A%A4%EC%9C%84%EC%B9%98")

    # load new pages
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # get parent elements of product info area
    element_list = browser.find_elements_by_xpath("""//ul/li/div[@class='productResultList']""")

    # print product information while iterating parent elements
    for element in element_list:

        product_title = element.find_element_by_xpath("""./div[2]/a""").text.encode("utf-8")
        product_price = element.find_element_by_xpath("""./div[3]/div[1]/span[1]/a[1]/strong""").text.encode("utf-8")

        scrap_time = time.strftime('%Y-%m-%d %H:%M:%S')
        market_data.append([site_title, product_title, product_price, scrap_time])
    
    print ("[INFO] InterPark crawl succeeded")
    return market_data

# Function that scrap product information at "TMON"
def tmon_crawling(browser, market_data):

    site_title = "TMON"

    browser.get("https://search.tmon.co.kr/search/?keyword=%EB%8B%8C%ED%85%90%EB%8F%84%20%EC%8A%A4%EC%9C%84%EC%B9%98")

    # load new pages
    for i in range(5):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # get parent elements of product info area
        element_list = browser.find_elements_by_xpath("//*[@id='search_app']/div[2]/section/div/ul/div/div/li/a/div[3]")

        # print product information while iterating parent elements
        for element in element_list:
            product_price = element.find_element_by_xpath("./div[@class='price_area']/span[@class='price']/span[@class='sale']/i[@class='num']").text.encode("utf-8")
            product_title = element.find_element_by_xpath("./p[@class='title']/strong[@class='tx']").text.encode("utf-8")

            print product_title, product_price
            scrap_time = time.strftime('%Y-%m-%d %H:%M:%S')
            market_data.append([site_title, product_title, product_price, scrap_time])
    
    print ("[INFO] TMON crawl succeeded")
    return market_data

def auction_crawling(browser, market_data):

    site_title = "Auction"

    for page_num in range(5):

        browser.get("http://browse.auction.co.kr/search?keyword=%EB%8B%8C%ED%85%90%EB%8F%84+%EC%8A%A4%EC%9C%84%EC%B9%98"+str(page_num + 1))

        # load new pages
        for i in range(3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        # get parent elements of product info area
        element_list = browser.find_elements_by_xpath("//*[@id='section--inner_content_body_container']/div[@module-design-id='17']/div[@class='component component--item_card type--general']/div[1]/div[1]/div[2]")

        # print product information while iterating parent elements
        for element in element_list:

            product_title = element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_title']/span/a/span[@class='text--brand']").text.encode("utf-8")
            product_title += element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_title']/span/a/span[@class='text--title']").text.encode("utf-8")
            
            product_price = element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_price']/span[@class='price_seller']/strong[@class='text--price_seller']").text.encode("utf-8")

            print product_title, product_price
            scrap_time = time.strftime('%Y-%m-%d %H:%M:%S')
            market_data.append([site_title, product_title, product_price, scrap_time])
    
    print ("[INFO] Auction crawl succeeded")
    return market_data

def insertData(market_data):

    db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     password = 'admin',
                     db = 'test',
                     charset = "utf8mb4"
                     )
     
    cursor = db.cursor()
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")

    sql = "INSERT INTO Nintendo_TB (shop, pname, price, pdate) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE price = %s, pdate = %s"

    for element in market_data:
        
        shop_name = str(element[0])
        # real product name
        product_name = element[1]
        # fake product name
        #product_name = " ".join(element[1].split()[1:])
        price = element[2]
        # real date
        date = element[3]
        # fake date
        #date = "2020-06-24 10:10:10"

        val = (shop_name, product_name, price, date, price, date)
        cursor.execute(sql, val)

        db.commit()

    db.close()

if __name__ == '__main__':

    # encoding proplem
    reload(sys)
    sys.setdefaultencoding('utf-8')

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("lang=ko_KR")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    browser = webdriver.Chrome(executable_path='/home/ubuntu/wannaKnowMarketPrice/chromedriver', chrome_options=options)

    # database array
    market_data = []

    # scrap information by site
    market_data = InterPark_crawling(browser, market_data)
    market_data = SSG_crawling(browser, market_data)
    market_data = tmon_crawling(browser, market_data)
    market_data = auction_crawling(browser, market_data)

    browser.quit()

    market_data = bigram.bigram_rank(market_data)

    insertData(market_data)
