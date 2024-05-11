#tkuim_2014_08
import csv
import pymysql
import json
import math
db_settings_file=open('src\db_setting.json','r')
db_settings=json.load(db_settings_file)

def add_member(member_id,member_name):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `members`(member_id,member_name)VALUE(%s,%s)"
            cursor.execute(
                command, (member_id,member_name)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def delete_member(member_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "DELETE FROM `members` WHERE member_id = %s"
            cursor.execute(command,(member_id))
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

def view_menu(shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM `shops` WHERE shop_id = %s"
            cursor.execute(
                command, (shop_id)
            )
            str=''
            for i in cursor:
                str=i[4]
            return str
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
                str+=i[0]+' : '+ i[1] + '\n'
                run_time_dic[i[0]]=i[1]
            str = str.rstrip()
            return str
    except Exception as ex:
        print(ex)

def order_detail(msg):
    msg=msg.split('\n')
    shop_name=msg[0]
    shop_id=check_shop_id(shop_name)[0]
    product_name=''
    product_number=''
    total_cost=0
    for row in msg[1:]:
        row=row.split(',')
        prouct_detail=check_product(shop_id,row[0])
        product_name+=str(prouct_detail[0])+','
        product_number+=row[1]+','
        total_cost+=float(prouct_detail[1])*float(row[1])
    round(total_cost,0)
    product_name = product_name.rstrip(',')
    product_number = product_number.rstrip(',')
    order_detail={
        'shop_id':str(shop_id),'product_name':str(product_name),'product_number':str(product_number),'total_cost':str(int(total_cost))
    }
    return order_detail

def check_product(shop_id,product_name):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM `menu` WHERE shop_id = %s AND product_name = %s"
            cursor.execute(
                command, (int(shop_id),product_name)
            )
            str=[]
            for i in cursor:
                str.append(i[1])
                str.append(i[3])
            return str
    except Exception as ex:
        print(ex)

def check_shop_id(shop_name):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM `shops` WHERE shop_name = %s"
            cursor.execute(
                command, (shop_name)
            )
            str=[]
            for i in cursor:
                str.append(i[0])
            return str
    except Exception as ex:
        print(ex)

def order_now(msg):
    order=order_detail(msg)
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "INSERT INTO `order_histories`(shop_id,product_name,product_number,total_cost)VALUE(%s,%s,%s,%s)"
            cursor.execute(
                command, (order['shop_id'],order['product_name'],order['product_number'],order['total_cost'])
            )
            conn.commit()
    except Exception as ex:
        print(ex)
'''
import chardet
with open('src\menu.csv', 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']
with open("src\menu.csv",newline='',encoding=encoding) as csvfile:
    count = 1
    shop_id=1
    menu = csv.DictReader(csvfile)
    for product in menu:
        if(int(product['shop_id'])!=shop_id):
            count=1
            shop_id+=1
        add_menu(int(product['shop_id']),product['product_name'],float(product['cost']),count)
        count+=1
'''

