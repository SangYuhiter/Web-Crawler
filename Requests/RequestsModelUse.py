# -*-coding:utf-8-*-

import requests


if __name__=="__main__":
    r=requests.get('https://www.baidu.com')
    print(type(r))
    print(r.status_code)
    print(r.text)
    print(type(r.text))
    print(r.cookies)