# -*-coding:utf-8-*-

import urllib.request


def Testurlopen(url):
    response = urllib.request.urlopen(url)
    # print(response.read().decode('utf-8'))
    print(type(response))
    print(response.status)
    print(response.getheaders())
    print(response.getheader('Server'))


if __name__=="__main__":
    url='https://www.python.org'
    Testurlopen(url)