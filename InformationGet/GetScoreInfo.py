# -*- coding:utf-8 -*-
# 此程序用于获取各高校录取分数

import requests
from bs4 import BeautifulSoup
from lxml import etree


# 哈尔滨工业大学
def get_score_info_hit():
    main_url = "http://zsb.hit.edu.cn/information/score"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划省份
    province = []
    for item in main_page_soup.find(class_="province").find_all(name='a'):
        province.append(item.string.strip())
    # print(province)
    # 招生计划年份
    years = []
    for item in main_page_soup.find_all(class_="year-select"):
        years.append(item.string.strip())
    # print(years)

    # 对每年份各省数据进行抽取
    for pro in province:
        for year in years:
            print("获取", year, pro, "的录取分数")
            # 构造链接
            specific_url = main_url + "?" + "year=" + year + "&" + "province=" + pro
            page_source = requests.get(specific_url).text
            page_soup = BeautifulSoup(page_source, "lxml")
            page_soup.prettify()
            # 表名
            table_name = page_soup.find(class_="info_line").text.strip()
            # print("表名:", table_name)
            # 表头
            table_head = []
            for item in page_soup.find(class_="info_table").thead.find_all(name="td"):
                table_head.append(item.string.strip())
            # print("表头:", table_head)
            # 表内容
            table_content = []
            for item in page_soup.find(class_="info_table").tbody.find_all(name="tr"):
                temp = []
                for sub_item in item.find_all(name="td"):
                    temp.append(sub_item.string.strip())
                table_content.append(temp)
            # for item in table_content:
            #     print(item)
            # 将表内容写入文本文件
            filepath = "九校联盟/哈尔滨工业大学/录取分数"
            with open(filepath + "/" + table_name, 'w', encoding='utf-8') as file:
                for item in table_head:
                    file.write(item + "\t")
                file.write("\n")
                for item in table_content:
                    for sub_item in item:
                        file.write(sub_item + "\t")
                    file.write("\n")
            print(year, pro, "的录取分数已存入文件")


# 北京大学
def get_score_info_pku():
    main_url = "http://www.gotopku.cn/programa/admitline/7"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划年份
    years = []
    for item in main_page_soup.find(class_="lqlist").find_all(name='a'):
        years.append(item.string.strip())
    print(years)

    for year in years:
        # 构造链接
        specific_url = main_url + "/" + year
        page_source = requests.get(specific_url).text
        page_soup = BeautifulSoup(page_source, "lxml")
        page_soup.prettify()

        # 表名
        table_name = year
        table_content = []
        print("表名:", table_name)
        # 表内容(原表)
        source_table_content = []
        for item in page_soup.find(class_="lqtable").find_all(name="td"):
            source_table_content.append(item.string)
        # 表头
        table_head = source_table_content[:5]
        print("表头:", table_head)
        source_table_content = source_table_content[5:]
        for i in range(0, len(source_table_content), 5):
            temp = []
            for j in range(5):
                if source_table_content[i + j] is None:
                    temp.append("-")
                    continue
                temp.append(source_table_content[i + j])
            table_content.append(temp)
        for item in table_content:
            print(item)

        # 将表内容写入文本文件
        filepath = "九校联盟/北京大学/录取分数"
        with open(filepath + "/" + table_name, 'w', encoding='utf-8') as file:
            for item in table_head:
                file.write(item + "\t")
            file.write("\n")
            for item in table_content:
                for sub_item in item:
                    file.write(sub_item + "\t")
                file.write("\n")


# 北京大学医学部
def get_score_info_pkuhsc():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/lnfs"
    page_urls = ["194116", "187052", "183832", "176388"]
    filepath = "九校联盟/北京大学/录取分数/医学部"

    # 2017年表
    # get_score_info_pkuhsc_table_2017(main_url,page_urls[0],filepath)
    # get_score_info_pkuhsc_table_2016(main_url, page_urls[1], filepath)
    get_score_info_pkuhsc_table_2015(main_url,page_urls[2],filepath)

# 北大医学部2017年表
def get_score_info_pkuhsc_table_2017(main_url,url,filepath):
    # 表1
    specific_url = main_url+"/"+url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    table_name = page_soup.find(class_="bt1").text
    print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={"style": "width: 888px; border-collapse: collapse"})\
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    print(table_head)
    table_content = table_content[1:]
    for item in table_content:
        print(item)
    write_table(filepath, table_name, table_head, table_content)

# 北大医学部2016年表
def get_score_info_pkuhsc_table_2016(main_url,url,filepath):
    # 表1
    specific_url = main_url+"/"+url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    table_name = page_soup.find(class_="bt1").text
    # print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={"style": "width: 1497px; border-collapse: collapse; margin: auto auto auto -0.25pt"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    # print(table_head)
    table_content = table_content[1:]
    # 去除表尾备注
    table_content = table_content[:-3]
    # for item in table_content:
    #     print(item)
    write_table(filepath, table_name, table_head, table_content)

    # 国家专项附表
    table_content=[]
    for item in page_soup.find(name="table", attrs={"style": "width: 898px; border-collapse: collapse"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    table_name="2016"+table_content[0][0]
    table_head=table_content[1]
    table_content=table_content[2:-1]
    for item in table_content:
        print(item)
    write_table(filepath, table_name, table_head, table_content)


# 北大医学部2015年表
def get_score_info_pkuhsc_table_2015(main_url,url,filepath):
    # 表1
    specific_url = main_url+"/"+url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    table_name = page_soup.find(class_="bt1").text
    print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={"style": "border-top: medium none; border-right: medium none; border-collapse: collapse; border-bottom: medium none; border-left: medium none"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    print(table_head)
    table_content = table_content[1:]
    # 去除表尾备注
    table_content = table_content[:-15]
    for item in table_content:
        print(item)
    write_table(filepath, table_name, table_head, table_content)

    print("------------------")
    # 国家专项附表
    table_content=[]
    for item in page_soup.find(name="table", attrs={"style": "width: 907px; border-collapse: collapse; margin: auto auto auto -0.25pt"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    table_name="2015"+table_content[0][0]
    table_head=table_content[1]
    print(table_name)
    print(table_head)
    table_content=table_content[2:-1]
    for item in table_content:
        print(item)
    write_table(filepath, table_name, table_head, table_content)


# 将表内容写入文本文件
def write_table(filepath, table_name, table_head, table_content):
    with open(filepath + "/" + table_name, 'w', encoding='utf-8') as file:
        for item in table_head:
            file.write(item + "\t")
        file.write("\n")
        for item in table_content:
            for sub_item in item:
                file.write(sub_item + "\t")
            file.write("\n")


if __name__ == "__main__":
    # get_score_info_hit()
    # get_score_info_pku()
    get_score_info_pkuhsc()