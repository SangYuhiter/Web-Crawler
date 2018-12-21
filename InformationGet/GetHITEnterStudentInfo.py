# -*- coding:utf-8 -*-

import requests

# 引入chromedriver,在python端打开浏览器
from selenium import webdriver
# chrome浏览器设置
from selenium.webdriver.chrome.options import Options
# 导入bs4包
from bs4 import BeautifulSoup

# 导入robots协议包
from urllib.robotparser import RobotFileParser

import os

# Chrome 后台模式
def LinkChromeHeadless(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')    # 禁用GPU加速
    browser = webdriver.Chrome(options=chrome_options)
    # 开始提交访问
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    soup.prettify()
    # 提取url链接
    main_page_url=[]
    for li in soup.body.div.find(class_='nav').ul.find_all(target='_self'):
        temp = []
        temp.append(li.string.strip())
        next_page_url = li['href']
        if (next_page_url[0:5]!='http:'):
            if(next_page_url[0:2] == '//'):
                next_page_url = 'http:'+next_page_url
            else:
                next_page_url=url+next_page_url
        temp.append(next_page_url)
        main_page_url.append(temp)
    # 进一步处理,去重和首页
    main_page_url.pop(0)
    main_page_url.pop(1)
    main_page_url.pop(9)
    for url in main_page_url:
        print(url)
    # 存入文本useurl.txt
    with open('useurl.txt','w',encoding='utf-8')as file:
        for url in main_page_url:
            file.write(url[0]+'\t'+url[1]+'\n')
    browser.close()


# 测试是否允许爬虫
def CrawlerRobots(url):
    rp = RobotFileParser()
    rp.set_url('http://www.hit.edu.cn/robots.txt')
    rp.read()
    print(rp.can_fetch('*', url))


#读取链接文件
def ReadUseurl(filepath):
    with open(filepath, 'r', encoding='utf-8')as file:
        urllines = file.readlines()
    return urllines


# 爬取文章界面
def GetArticlePage(pageurl,filemkdir):
    pagesource=requests.get(pageurl).text
    soup = BeautifulSoup(pagesource, 'lxml')
    soup.prettify()
    articleurls=[]
    for articleurl in soup.body.find(class_='second_container').find(class_='right_content').find_all(name='a'):
        temp=[]
        temp.append(articleurl.string.strip())
        temp.append('http:'+articleurl['href'])
        articleurls.append(temp)
    articleurls.pop(0)
    with open(filemkdir+'/urls.txt','w',encoding='utf-8')as file:
        for url in articleurls:
            file.write(url[0]+'\t'+url[1]+'\n')
    return articleurls

def CreatMkdir():
    filepath = 'useurl.txt'
    urllines=ReadUseurl(filepath)
    for urlline in urllines:
        name_url = urlline.split('\t')
        name = name_url[0]
        url = name_url[1].strip()
        print(name, url)
        # 创建资料文件夹
        if not os.path.exists('Information\\'+name):
            os.makedirs('Information\\'+name)

def SearchInformation():
    url = 'http://zsb.hit.edu.cn/article/category/b4d5b3b1ffc2bb012fb52138b25a824b'
    filemkdir = 'Information/报考指南'
    articleurls = GetArticlePage(url, filemkdir)
    for artic in articleurls:
        download_page = artic
        download_page_source = requests.get(download_page[1]).text
        download_page_soup = BeautifulSoup(download_page_source, 'lxml')
        download_page_soup.prettify()
        for line in download_page_soup.find_all(name='p'):
            with open(filemkdir + '/' + download_page[0] + '.txt', 'a', encoding='utf-8')as file:
                if (line.text != ''):
                    file.write(line.text + '\n')


def GetInfomationURLs():
    topmenus = ReadUseurl('useurl.txt')
    infomation = []
    for menu in topmenus:
        menu_name = menu.split('\t')[0]
        menu_url = menu.split('\t')[1].strip()
        # print(menu_name,menu_url)
        temp = []
        for info in menu_url.split('/'):
            # 提取含infomation的链接
            if info == 'information':
                temp.append(menu_name)
                temp.append(menu_url)
                infomation.append(temp)
            # 去除录取查询的链接
            if info == 'admission-query':
                temp.append(menu_name)
                temp.append(menu_url)
                infomation.remove(temp)
    print(infomation)
    return infomation

def GetProvinceInfo():
    infomation = GetInfomationURLs()
    for menu in infomation:
        menu_name = menu[0]
        menu_url = menu[1].strip()
        # 存储文件位置
        store_file_path = 'Infomation//' + menu_name
        province_page_source = requests.get(menu_url).text
        province_page_soup = BeautifulSoup(province_page_source, 'lxml')
        province_page_soup.prettify()
        print(province_page_soup.body.find(class_='second_container').find(class_='right_content'))


# 获取学院、专业介绍
def GetCollegeInfo():
    main_page_url='http://zsb.hit.edu.cn/article/read/f2c5136702307bbba768e96e4b5031b3'
    main_page_name='专业介绍'
    # 获取主界面源码
    main_page_source=requests.get(main_page_url).text
    main_page_soup=BeautifulSoup(main_page_source,'lxml')
    main_page_soup.prettify()

    # 获取学院、专业链接
    colloge=[]
    for link in main_page_soup.find(class_='article_content').find_all(name='a'):
        colloge.append(link)
    # for link in colloge:
    #     print(link)
    return colloge


# 获取具体页面文字信息
def GetWordInfo(page_url, page_name):
    page_source = requests.get(page_url).text
    page_soup = BeautifulSoup(page_source, 'lxml')
    page_soup.prettify()
    print(page_soup.text)
    # for line in page_soup.find_all(name='p'):
    #     print(line.string)
if __name__ == "__main__":
    colloge=GetCollegeInfo()
    page_url=colloge[0]['href']
    page_name=colloge[0].string
    GetWordInfo(page_url,page_name)
    # import tesserocr
    # print(tesserocr.file_to_text('image.png'))
