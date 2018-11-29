# -*- encoding:utf-8 -*-


# 引入chromedriver,在python端打开浏览器
from selenium import webdriver
# chrome浏览器设置
from selenium.webdriver.chrome.options import Options


# Chrome 页面模式
def LinkChromePage(url):
    browser = webdriver.Chrome()
    browser.get(url)
    print(url)
    browser.close()


# Chrome 后台模式
def LinkChromeHeadless(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')    # 禁用GPU加速
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    print(browser.current_url)
    browser.close()


if __name__=='__main__':
    url = 'http://www.baidu.com'
    # LinkChromePage(url)
    LinkChromeHeadless(url)