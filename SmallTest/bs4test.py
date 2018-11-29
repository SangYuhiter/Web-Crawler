# -*- coding:utf-8 -*-

# 导入bs4包
from bs4 import BeautifulSoup


# bs4 Test
def bs4Test():
    soup = BeautifulSoup('<p>Hello</p>', 'lxml')
    print(soup.p.string)


if __name__ == '__main__':
    bs4Test()