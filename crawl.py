#-*- coding:utf-8 -*-

# we may not use bs4 and requests...
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Function that scrap product information at "NAVER Shopping"
def naver_shopping_crawling(browser):

    print "\n\n<Naver Crawling Result>\n\n"
    browser.get("https://search.shopping.naver.com/search/all.nhn?query=%EB%8B%8C%ED%85%90%EB%8F%84+%EC%8A%A4%EC%9C%84%EC%B9%98")

    # [todo] add loading command
    time.sleep(2)

    element_list = browser.find_elements_by_xpath("//*[@id='_search_list']/div[1]/ul/li/div[@class='info']")

    # print product information while iterating parent elements
    for element in element_list:
        # product price has two types of tag at NAVER Shopping
        # so, we have to check two tags
        try:
            product_price = element.find_element_by_xpath("./span[@class='price']/em/span[@class='num _price_reload']").text.encode('utf-8')
        except:
            product_price = element.find_element_by_xpath("./span[@class='price']/em/span[@class='num']").text.encode('utf-8')
        product_title = element.find_element_by_xpath("./div[@class='tit']/a").text.encode('utf-8')

        print product_title
        print product_price
        print "-----------------------------------"
    
    return


# Function that scrap product information at "TMON"
def tmon_crawling(browser):

    print "\n\n<TMON Crawling Result>\n\n"
    browser.get("https://search.tmon.co.kr/search/?keyword=%EB%8B%8C%ED%85%90%EB%8F%84%20%EC%8A%A4%EC%9C%84%EC%B9%98")

    # load new pages
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # get parent elements of product info area
    element_list = browser.find_elements_by_xpath("//*[@id='search_app']/div[2]/section/div/ul/div/div/li/a/div[3]")

    # print product information while iterating parent elements
    for element in element_list:
        product_price = element.find_element_by_xpath("./div[@class='price_area']/span[@class='price']/span[@class='sale']/i[@class='num']").text.encode('utf-8')
        product_title = element.find_element_by_xpath("./p[@class='title']/strong[@class='tx']").text.encode('utf-8')

        print product_title
        print product_price
        print "-----------------------------------"
    
    return

def auction_crawling(browser):

    print "\n\n<Auction Crawling Result>\n\n"
    browser.get("http://browse.auction.co.kr/search?keyword=%EB%8B%8C%ED%85%90%EB%8F%84+%EC%8A%A4%EC%9C%84%EC%B9%98")

    # load new pages
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # get parent elements of product info area
    element_list = browser.find_elements_by_xpath("//*[@id='section--inner_content_body_container']/div[@module-design-id='17']/div[@class='component component--item_card type--general']/div[1]/div[1]/div[2]")

    # print product information while iterating parent elements
    for element in element_list:

        product_title = element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_title']/span/a/span[@class='text--brand']").text.encode('utf-8')
        product_title += element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_title']/span/a/span[@class='text--title']").text.encode('utf-8')
        
        product_price = element.find_element_by_xpath("./div[1]/div[@class='area--itemcard_price']/span[@class='price_seller']/strong[@class='text--price_seller']").text.encode('utf-8')

        print product_title
        print product_price
        print "-----------------------------------"
    
    return

if __name__ == '__main__':
    
    options = Options()
    options.headless = True

    # we use Firefox for scrapping
    browser = webdriver.Firefox(options=options)

    # scrap information by site
    naver_shopping_crawling(browser)
    tmon_crawling(browser)
    auction_crawling(browser)

    browser.quit()
