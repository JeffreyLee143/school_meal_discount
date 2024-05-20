#tkuim_2014_08
import csv
import pymysql
import json
import math
import time
import datetime
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

def delete_order(order_id,time):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT trade_date FROM `order_histories` WHERE order_id = %s"
            cursor.execute(
                command, (int(order_id),)
            )
            datetime1 = cursor.fetchone()[0]
            datetime2 = datetime.datetime.fromtimestamp(time/1000)
            timedelta = datetime2 - datetime1
            if(timedelta > datetime.timedelta(minutes=1)):
                message='店家已經接收並開始製作訂單\n故無法取消'
                return message
            elif(timedelta<=datetime.timedelta(minutes=1)):
                command = "DELETE FROM `order_histories` WHERE order_id = %s"
                cursor.execute(
                    command, (int(order_id),)
                )
                conn.commit()
                message='刪除成功'
                return message
    except Exception as ex:
        print(ex)

def view_order(order_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM `order_histories` WHERE order_id=%s"
            cursor.execute(
                command, (int(order_id))
            )
            if len(cursor.fetchall()) == 0:
                return '沒有此訂單，請確認訂單id是否有打對\n'
            else:
                str=[]
                for i in cursor._rows:
                    str.append(i[1])
                    str.append(i[3])
                    str.append(i[4])
                menu = order_name(str[0], str[1], str[2])
                return menu
    except Exception as ex:
        print(ex)

def order_name(shop_id, product_name, product_number):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT shop_name FROM `shops` WHERE shop_id=%s"
            cursor.execute(command, (int(shop_id),))
            result=[]
            result.append(cursor.fetchone()[0])
            if(len(product_name)>1):
                name_num=product_name.split(',')
                num=product_number.split(',')
            else:
                name_num=product_name
                num=product_number
            for i in range(len(name_num)):
                command = "SELECT product_name FROM `menu` WHERE product_id IN (%s)"
                cursor.execute(command,(int(name_num[i])))
                result.append(cursor.fetchone()[0])
            for i in range(len(num)):
                result[i+1] += '*'
                result[i+1] += num[i]
            menu = '\n'.join(result)
            return menu
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
            command = "SELECT `order_id` FROM `order_histories` WHERE shop_id = %s AND product_name = %s ORDER BY `order_id` DESC LIMIT 1"
            cursor.execute(
                command, (order['shop_id'],order['product_name'])
            )
            for i in cursor:
                return str(i[0])
    except Exception as ex:
        print(ex)

def discount_information():
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT discount_content FROM discounts;"
            cursor.execute(command)
            str=''
            for i in cursor:
                str+=i[0]+ '\n'
            str = str.rstrip()
            return str
    except Exception as ex:
        print(ex)

def add_discount(id,content,discount):
    try:
       conn = pymysql.connect(**db_settings)
       cursor = conn.cursor()
       with conn.cursor() as cursor:
            command = "INSERT INTO `discount`(id,content,discount)VALUE(%s,%s,%s)"
            cursor.execute(
                command, (id,content,discount)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def delete_discount(id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "DELETE FROM `discount` WHERE id = %s"
            cursor.execute(command,(id))
            conn.commit()
    except Exception as ex:
        print(ex)

def add_point(id,price):
    try:
       member_point=price/50 #設定每消費50元可獲得一點
       conn = pymysql.connect(**db_settings)
       cursor = conn.cursor()
       with conn.cursor() as cursor:
            command =  "UPDATE members SET member_point = member_point+%s WHERE member_id = %s"
            cursor.execute(
                command, (int(member_point),id)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def spend_point(member_id, member_point):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            # 查詢指定會員號的資料
            cursor.execute("SELECT member_point FROM members WHERE member_id = %s", (member_id,))
            result = cursor.fetchone()
            if result is None:
                print("Member not found.")
                return
            # 獲取並檢查當前的積分
            current_point = result[0]  # 使用索引0來獲取'point'欄位的值
            if current_point == 0:
                print('This member has no points')
                return
            if current_point < member_point:
                print('Not enough points')
                return
            # 更新積分
            command = "UPDATE members SET member_point = member_point - %s WHERE member_id = %s"
            cursor.execute(command, (member_point, member_id))
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
add_point('U5331a53d095a53d040a15a0481c6945c',150)