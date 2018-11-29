# -*- encoding:utf-8 -*-

from selenium import webdriver


# Phantomjs 无页面的浏览器,会报warning，新版本的selenium不支持Phantomjs,使用chrome的无页面模式
def LinkPhantomjs(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    print(browser.current_url)


if __name__=='__main__':
    url='http://www.baidu.com'
    LinkPhantomjs(url)