# -*- coding:utf-8 -*-
# 此程序用于创建MySQL数据库
import mysql.connector
import requests
from bs4 import BeautifulSoup


# 连接数据库
def connect_mysql():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="university_admission"
    )
    return mydb


# 插入哈工大招生数据
def insert_admission_plan_hit():
    main_url = "http://zsb.hit.edu.cn/information/plan"
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
            print("获取", year, pro, "的招生计划")
            # 构造链接
            specific_url = main_url + "?" + "year=" + year + "&" + "province=" + pro
            page_source = requests.get(specific_url).text
            page_soup = BeautifulSoup(page_source, "lxml")
            page_soup.prettify()
            # 表名
            table_name = page_soup.find(class_="info_line").string
            print("表名:", table_name)
            # 表头
            table_head = []
            for item in page_soup.find(class_="info_table").thead.find_all(name="td"):
                table_head.append(item.string.strip())
            print("表头:", table_head)
            # 表内容
            table_content = []
            for item in page_soup.find(class_="info_table").tbody.find_all(name="tr"):
                temp = []
                for sub_item in item.find_all(name="td"):
                    temp.append(sub_item.string.strip())
                table_content.append(temp)
            # for item in table_content:
            #     print(item)
            for item in table_content:
                if len(item) == 3:
                    if item[1] == "统计":
                        table_content.remove(item)
            mysql_content = []
            for item in table_content:
                if len(item) != 3:
                    break
                temp = ("哈尔滨工业大学", pro, item[0], year, item[1], item[2])
                mysql_content.append(temp)
            mydb = connect_mysql()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT MAX(id) FROM admission_plan")
            maxid = mycursor.fetchone()[0] + 1
            mysql_content = []
            for item in table_content:
                if len(item) != 3:
                    break
                temp = (maxid, "哈尔滨工业大学", pro, item[0], year, item[1], item[2])
                maxid+=1
                mysql_content.append(temp)
            sql_string = "INSERT INTO admission_plan(id,school,district,major,year,classy,numbers) " \
                         "VALUES (%s,%s,%s,%s,%s,%s,%s)"
            mycursor.executemany(sql_string, mysql_content)
            mydb.commit()
            # for item in mysql_content:
            #     print(item)
            print(table_name, "记录插入成功！")


# 插入北大招生计划数据
def insert_admission_plan_pku():
    main_url = "http://www.gotopku.cn/programa/enrolstu/6.html"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划科别（文理）
    familes = []
    contents = main_page_soup.find(class_="lqlist").contents
    for item in contents[1].find_all(name='a'):
        familes.append(item.string.strip())
    print(familes)
    # 招生计划年份
    years = []
    for item in contents[3].find_all(name='a'):
        years.append(item.string.strip())
    print(years)
    # 招生计划地区
    district = []
    for item in main_page_soup.find(class_="kr").find_all(name='a'):
        district.append(item.string.strip())
    print(district)

    # 构造链接
    for year in years:
        for i_district in range(len(district)):
            table_content = []
            for i_families in range(len(familes)):
                new_main_url = "http://www.gotopku.cn/programa/enrolstu/6"
                specific_url = new_main_url + "/" + year + "/" + str(i_district + 1) + "/" + str(i_families) + ".html"
                page_source = requests.get(specific_url).text
                page_soup = BeautifulSoup(page_source, "lxml")
                page_soup.prettify()
                # 表名
                table_name = year + district[i_district]
                print("表名:", table_name)
                # 表内容(原表)
                source_table_content = []
                for item in page_soup.find(class_="lqtable").find_all(name="td"):
                    source_table_content.append(item.string.strip())
                # 表头
                table_head = source_table_content[:2]
                table_head.insert(1, "类别")
                print("表头:", table_head)
                source_table_content = source_table_content[4:]
                for i in range(0, len(source_table_content), 2):
                    temp = []
                    temp.append(source_table_content[i])
                    if i_families == 0:
                        temp.append("文史")
                    else:
                        temp.append("理工")
                    temp.append(source_table_content[i + 1])
                    table_content.append(temp)
                mydb = connect_mysql()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT MAX(id) FROM admission_plan")
                maxid = mycursor.fetchone()[0] + 1
                mysql_content = []
                for item in table_content:
                    temp = (maxid, "北京大学", district[i_district], item[0], year, item[1], item[2])
                    maxid = maxid + 1
                    mysql_content.append(temp)
                sql_string = "INSERT INTO admission_plan(id,school,district,major,year,classy,numbers) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s)"
                mycursor.executemany(sql_string, mysql_content)
                mydb.commit()
                for item in mysql_content:
                    print(item)


# 插入北大医学部招生计划数据(2017\2016,2015无数据)
def insert_admission_plan_pkuhsc():
    insert_admission_plan_pkuhsc_2017()
    insert_admission_plan_pkuhsc_2016()


# 插入北大医学部招生计划数据2017
def insert_admission_plan_pkuhsc_2017():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/zsjh"
    year = "2017"
    # 构造链接
    specific_url = main_url + "/" + year + "/"
    print(specific_url)
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    year_and_district = page_soup.find_all(class_="link_new01")
    district = []
    district_url = []
    for item in year_and_district[1].find_all(name='a'):
        district.append(item.string.strip())
        district_url.append(item['href'])
    print(district)
    print(district_url)
    for i_url in range(len(district_url)):
        if (district[i_url] == "新疆预科" or district[i_url] == "内蒙古预科" or district[i_url] == "新疆西藏内地班"):
            break
        table_source = requests.get(specific_url + district_url[i_url])
        table_source.encoding = "utf-8"
        table_soup = BeautifulSoup(table_source.text, "lxml")
        table_soup.prettify()
        table_content = []
        for item in table_soup.find(class_="box_new02").table.tbody.find_all(name="tr"):
            temp = []
            for sub_item in item.find_all(name="td"):
                temp.append(sub_item.text.strip())
                # print(sub_item.text.strip())
            temp.pop(0)
            table_content.append(temp)
        table_name = year + district[i_url]
        table_head = table_content[0]
        table_content = table_content[1:]
        mydb = connect_mysql()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MAX(id) FROM admission_plan")
        maxid = mycursor.fetchone()[0] + 1
        for item in table_content:
            print(item)
        mysql_content = []
        for item in table_content:
            temp = (maxid, "北京大学", district[i_url], item[0] + item[1] + "年", year, "医科", item[2])
            maxid = maxid + 1
            mysql_content.append(temp)
        sql_string = "INSERT INTO admission_plan(id,school,district,major,year,classy,numbers) " \
                     "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        mycursor.executemany(sql_string, mysql_content)
        mydb.commit()
        print(table_name)
        print(table_head)
        for item in mysql_content:
            print(item)


# 插入北大医学部招生计划数据2016
def insert_admission_plan_pkuhsc_2016():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/zsjh"
    year = "2016"
    # 构造链接
    specific_url = main_url + "/" + year + "/"
    print(specific_url)
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    year_and_district = page_soup.find_all(class_="link_new01")
    district = []
    district_url = []
    for item in year_and_district[1].find_all(name='a'):
        district.append(item.string.strip())
        district_url.append(item['href'])
    print(district)
    print(district_url)
    for i_url in range(len(district_url)):
        if (district[i_url] == "新疆预科" or district[i_url] == "内蒙古预科" or district[i_url] == "新疆西藏内地班"):
            break
        table_source = requests.get(specific_url + district_url[i_url])
        table_source.encoding = "utf-8"
        table_soup = BeautifulSoup(table_source.text, "lxml")
        table_soup.prettify()
        table_content = []
        for item in table_soup.find(class_="box_new02").table.tbody.find_all(name="tr"):
            temp = []
            for sub_item in item.find_all(name="td"):
                temp.append(sub_item.text.strip())
                # print(sub_item.text.strip())
            table_content.append(temp)
        table_name = year + district[i_url]
        table_head = table_content[0]
        table_content = table_content[1:]
        mydb = connect_mysql()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MAX(id) FROM admission_plan")
        maxid = mycursor.fetchone()[0] + 1
        for item in table_content:
            print(item)
        mysql_content = []
        for item in table_content:
            temp = (maxid, "北京大学", district[i_url], item[0] + item[1] + "年", year, "医科", item[2])
            maxid = maxid + 1
            mysql_content.append(temp)
        sql_string = "INSERT INTO admission_plan(id,school,district,major,year,classy,numbers) " \
                     "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        mycursor.executemany(sql_string, mysql_content)
        mydb.commit()
        print(table_name)
        print(table_head)
        for item in mysql_content:
            print(item)


# 创建招生计划表
def create_admission_plan_table():
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE admission_plan("
                     "id INT PRIMARY KEY NOT NULL ,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "major VARCHAR(30),"
                     "year INT,"
                     "classy varchar(10),"
                     "numbers INT)")


# 创建录取分数表
def create_admission_score_table():
    mydb=connect_mysql()
    mycursor=mydb.cursor()
    # 各省的高校分数线(学校、地区、年份、类别、批次、最低分、最高分)
    mycursor.execute("CREATE TABLE admission_score_pro("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "classy varchar(10),"
                     "batch varchar(30),"
                     "lowest INT,"
                     "highest INT,"
                     "average INT)")
    # 高校的专业分数线
    mycursor.execute("CREATE TABLE admission_score_major("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "major VARCHAR(30),"
                     "year INT,"
                     "classy varchar(10),"
                     "lowest INT,"
                     "highest INT,"
                     "average INT,"
                     "amount INT)")


# 插入哈工大录取分数数据
def insert_admission_score_hit():
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
    mysql_content = []
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
            for item in table_content:
                if item[1]=="统计":
                    table_content.remove(item)
            for item in table_content:
                temp = ("哈尔滨工业大学", pro, item[0], year, item[1], item[4], item[2], item[3], item[5])
                mysql_content.append(temp)
            for item in mysql_content:
                print(item)
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    # mycursor.execute("TRUNCATE admission_score_major")
    sql_string = "INSERT INTO admission_score_major(school,district,major,year,classy,lowest,highest,average,amount) " \
                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql_string, mysql_content)
    mydb.commit()
    print("数据插入完成")



# 插入北大录取分数数据
def insert_admission_score_pku():
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

    mysql_content=[]
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
            source_table_content.append(str(item.string))
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
            if(item[2]!="-" and item[3]!="-"):
                temp=("北京大学",item[0],year,"文史",item[1],item[2],None,None)
                mysql_content.append(temp)
                temp = ("北京大学", item[0], year, "理工", item[1], item[3], None, None)
                mysql_content.append(temp)
            elif(item[2]!="-"and item[3]=="-"):
                temp = ("北京大学", item[0], year, "文史", item[1], item[2], None, None)
                mysql_content.append(temp)
            elif(item[2]=="-"and item[3]!="-"):
                temp = ("北京大学", item[0], year, "理工", item[1], item[3], None, None)
                mysql_content.append(temp)
            elif(item[2]=="-" and item[3]=="-" and item[4]!="-"):
                temp = ("北京大学", item[0], year, "其他", item[1], item[4], None, None)
                mysql_content.append(temp)
        for item in mysql_content:
            print(item)
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    # mycursor.execute("TRUNCATE admission_score_pro")
    sql_string = "INSERT INTO admission_score_pro(school,district,year,classy,batch,lowest,highest,average) " \
                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql_string, mysql_content)
    mydb.commit()
    print("数据插入完成")
if __name__ == "__main__":
    # insert_admission_plan_hit()
    # insert_admission_plan_pku()
    # insert_admission_plan_pkuhsc()
    # insert_admission_score_hit()
    insert_admission_score_pku()
    # create_admission_score_table()
