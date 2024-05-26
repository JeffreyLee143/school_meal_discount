import random
import csv
import pymysql
import json
import math
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')
#import chardet
db_settings_file=open('D:\school_meal_discount\src\db_setting.json','r')
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

def member_information(member_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT * FROM `members` WHERE member_id=%s"
            cursor.execute(command,(member_id))
            member_detail=''
            for i in cursor._rows:
                member_detail='註冊日期: '+str(i[2])+'\n會員名稱: '+str(i[3])+'\n持有點數: '+str(i[4])
            return member_detail
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
                command, (int(order_id),)
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
            num=[]
            result.append(cursor.fetchone()[0])
            if(len(product_name)>1):
                name_num=product_name.split(',')
                num=product_number.split(',')
            else:
                name_num=product_name
                num.append(product_number)
            for i in range(len(name_num)):
                command = "SELECT product_name FROM `menu` WHERE product_id = %s AND shop_id=%s"
                cursor.execute(command,(int(name_num[i]),int(shop_id)))
                result.append(cursor.fetchone()[0])
            if(len(num)>1):
                for i in range(len(num)):
                    result[i+1] += '*'
                    result[i+1] += num[i]
            else:
                result[1] += '*'
                result[1] += num[0]
            menu = '\n'.join(result)
            return menu
    except Exception as ex:
        print(ex)

def unfinish_order(shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT order_id FROM `order_histories` WHERE shop_id = %s and order_status = FALSE"
            cursor.execute(command, (int(shop_id),))
            results = cursor.fetchall()
            orders = [str(row[0]) for row in results]
            orders_str = ", ".join(orders)
            return orders_str
    except Exception as ex:
        print(ex)

def finish_order(order_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "UPDATE order_histories SET order_status = TRUE WHERE order_id = %s"
            cursor.execute(
                command, (int(order_id),)
            )
            conn.commit()
    except Exception as ex:
        print(ex)
        
def check_order_finish(order_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT order_status FROM `order_histories` WHERE order_id = %s "
            cursor.execute(
                command, (int(order_id),)
            )
            results = cursor.fetchone()[0]
            return results
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
    msg_lines = msg.split('\n')
    shop_name = msg_lines[0].strip()
    shop_id = check_shop_id(shop_name)[0]
    product_name = ''
    product_number = ''
    total_cost = 0
    total_points = 0
    # 移除空行
    msg_lines = [line for line in msg_lines if line.strip() != '']
    print(msg_lines)
    for row1 in msg_lines[1:]:
        row2 = [line.split('，') for line in row1.split(',')]
        row = [item.strip() for sublist in row2 for item in sublist if item.strip() != '']
        print(row)
        if len(row) < 3:
            raise ValueError('每行必須包含商品名稱、數量和欲使用點數')
        product_detail = check_product(shop_id, row[0])
        product_name += str(product_detail[0]) + ','
        product_number += row[1] + ','
        try:
            quantity = float(row[1])
            points_to_use = int(row[2])
        except ValueError:
            raise ValueError('數量必須是數字，欲使用點數必須是整數')
        total_cost += float(product_detail[1]) * quantity
        total_points += points_to_use
    total_cost = round(total_cost, 0)
    product_name = product_name.rstrip(',')
    product_number = product_number.rstrip(',')
    order_detail = {
        'shop_id': str(shop_id),
        'product_name': str(product_name),
        'product_number': str(product_number),
        'total_cost': (int(total_cost)),
        'total_points': int(total_points)
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
            print(str)
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

def order_now(msg,id):
    try:
        order=order_detail(msg)
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            if(spend_point(id,order['total_points'])):
                order['total_cost']-=order['total_points']
            command = "INSERT INTO order_histories(shop_id,product_name,product_number,total_cost)VALUE(%s,%s,%s,%s)"
            cursor.execute(
                command, (order['shop_id'],order['product_name'],order['product_number'],str(order['total_cost']))
            )
            conn.commit()
            command = "SELECT order_id FROM order_histories WHERE shop_id = %s AND product_name = %s ORDER BY order_id DESC LIMIT 1"
            cursor.execute(
                command, (order['shop_id'],order['product_name'])
            )
            add_point(id,order['total_cost']/50)
            for i in cursor:
                return str(i[0])
    except Exception as ex:
        print(ex)

def check_order(shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT COUNT(*) FROM `order_histories` WHERE shop_id = %s"
            cursor.execute(
                command, int(shop_id),
            )
            row = cursor.fetchone()[0]
            return row
    except Exception as ex:
        print(ex)

def get_order_id(shop_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT order_id FROM `order_histories` WHERE shop_id = %s ORDER BY order_id DESC LIMIT 1"
            cursor.execute(
                command, int(shop_id),
            )
            row = cursor.fetchone()[0]
            return row
    except Exception as ex:
        print(ex)

def get_point(member_id):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT member_point FROM `members` WHERE member_id = %s ORDER BY order_id DESC LIMIT 1"
            cursor.execute(
                command, int(member_id),
            )
            row = cursor.fetchone()[0]
            return row
    except Exception as ex:
        print(ex)

def add_point(id,point):  
    conn = pymysql.connect(**db_settings)
    try:
       cursor = conn.cursor()
       with conn.cursor() as cursor:
            command =  "UPDATE members SET member_point = member_point+%s WHERE member_id = %s"
            cursor.execute(
                command, (point,id)
            )
            conn.commit()
    except Exception as ex:
        print(ex)

def spend_point(member_id, point):
    conn = pymysql.connect(**db_settings)
    try:
        with conn.cursor() as cursor:
            # 查詢指定會員號的資料
            cursor.execute("SELECT member_point FROM members WHERE member_id = %s", (member_id,))
            result = cursor.fetchone()
            if result is None:
                print("Member not found.")
                return
            # 獲取並檢查當前的積分
            current_point = result[0]  # 使用索引0來獲取'point'欄位的值
            if(current_point<point):
                return False
            # 更新積分
            command = "UPDATE members SET member_point = member_point - %s WHERE member_id = %s"
            cursor.execute(command, (point, member_id))
            conn.commit()
            return True
    except Exception as ex:
        print(ex)                
 
def draw_discount(member_amount,point):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM members")# 查詢會員數量
            total_member = cursor._rows[0]
            total_member=total_member[0]#tuple轉成int
            draw_list=random.sample(range(1,total_member+1),member_amount)#生成中獎名單
            draw_list.sort()#排序
            for i in draw_list:
                command = "SELECT member_id FROM members LIMIT %s,%s"
                cursor.execute(
                    command, (i-1,1)#抓取會員id
                )
                member_id=cursor._rows[0]
                add_point(member_id[0],point*20)#引用add_point新增點數
    except Exception as ex:
        print(ex)

def lottery(id,point):
    rate=random.randint(0,100)
    str=[]
    str.append(rate)
    if(rate>60):
        point=point*((1+(rate-60)/100))
        add_point(id,int(point))
        str.append(int(point))
    else:
        str.append(0)
    return str

'''        
def draw_discount(member_amount,point):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM members")# 查詢會員數量
            total_member = cursor._rows[0]
            total_member=total_member[0]#tuple轉成int
            draw_list=random.sample(range(1,total_member+1),member_amount)#生成中獎名單
            draw_list.sort()#排序
            for i in draw_list:
                command = "SELECT member_id FROM members LIMIT %s,%s"
                cursor.execute(
                    command, (i-1,1)#抓取會員id
                )
                member_id=cursor._rows[0]
                add_point(member_id[0],point*20)#引用add_point新增點數
    except Exception as ex:
        print(ex)
''' 
#with open('C:\\Users\\USER\\Desktop\\school_menu_discount\\menu.csv', 'rb') as f:
#    result = chardet.detect(f.read())
#    encoding = result['encoding']
#with open("C:\\Users\\USER\\Desktop\\school_menu_discount\\menu.csv",newline='',encoding=encoding) as csvfile:
#    count = 1
#    shop_id=1
#    menu = csv.DictReader(csvfile)
#    for product in menu:
#        if(int(product['shop_id'])!=shop_id):
#            count=1
#            shop_id+=1
#        add_menu(int(product['shop_id']),product['product_name'],float(product['cost']),count)
#        count+=1
#print(view_order(22))