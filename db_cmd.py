#tkuim_2014_08
import csv
import pymysql
import json
db_settings_file=open('src\db_setting.json','r')
db_settings=json.load(db_settings_file)

def add_member(member_number,member_name,member_mail):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `members`(member_number,member_name,member_mail)VALUE(%s,%s,%s)"
            cursor.execute(
                command, (member_number,member_name,member_mail)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def delete_member(member_mail):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "DELETE FROM `members` WHERE member_mail = %s"
            cursor.execute(command,(member_mail))
            conn.commit()
    except Exception as ex:
        print(ex)

def add_shop(shop_name):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `shops`(shop_name)VALUE(%s)"
            cursor.execute(
                command, (shop_name)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def delete_shop(shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "DELETE FROM `shops` WHERE shop_id = %s"
            cursor.execute(command,(shop_id))
            conn.commit()
    except Exception as ex:
        print(ex)

def add_order(shop_id,product_name,total_cost):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `order_histories`(shop_id,product_name,total_cost)VALUE(%s,%s,%s)"
            cursor.execute(
                command, (int(shop_id),product_name,int(total_cost))
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def delete_order(order_id,shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "DELETE FROM `order_histories` WHERE order_id = %s AND shop_id= %s"
            cursor.execute(
                command, (int(order_id),int(shop_id))
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def add_menu(shop_id,product_name,product_price,count):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `menu`(shop_id,product_name,product_price,product_id)VALUE(%s,%s,%s,%s)"
            cursor.execute(
                command, (shop_id,product_name,product_price,count)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def run_time():
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT shop_name,shop_run_time FROM shops;"
            cursor.execute(command)
            run_time_dic={}
            str=''
            for i in cursor:
                str=str+i[0]+' : '+ i[1] + '\n'
                run_time_dic[i[0]]=i[1]
            return str
    except Exception as ex:
        print(ex)
'''
import chardet
with open('src\menu.csv', 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']
with open("src\menu.csv",newline='',encoding=encoding) as csvfile:
    count = 1
    menu = csv.DictReader(csvfile)
    for product in menu:
        add_menu(int(product['shop_id']),product['product_name'],float(product['cost']),count)
        count+=1
'''


#shop_name = {"早安美廣","傳香飯糰","八方雲集","宜廷小吃","琪美食堂","美廣鮮果吧","自助餐"}
#for i in shop_name:
#    add_shop(i)
#add_member("09123456789","Jeffrey","anb@gmail.com")
#delete_member("anb@gmail.com")
#delete_shop("big_shop@gmail.com")
#add_order(1,"'蛋餅',2,'巧克力',3",5000)
#delete_order(1,1)
