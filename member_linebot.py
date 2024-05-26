from flask import Flask, request, abort
from pyngrok import ngrok, conf
from linebot.webhook import WebhookHandler
from linebot import LineBotApi
from linebot.v3.exceptions import InvalidSignatureError
from linebot.models import *
import json
import matplotlib.pyplot as plt
import matplotlib.image as img
import db_cmd 
from time import sleep
import threading
db_settings_file=open('src\db_setting.json','r')
db_settings=json.load(db_settings_file)
ngrok_path = 'src\\ngrok.exe'
conf.get_default().ngrok_path=ngrok_path
conf.get_default().auth_token = '2fzU7K2oDcw4rNQ4i8JMEoZrzpV_28yEF9t59wiXrMQULEBA7'
#conf.get_default().auth_token = getpass.getpass(auth)

class Msg_package:
    now_id=0
    msg='' #保存使用者訊息
    flag=-1 #判斷是否被占用
    user_id=''

# Open a TCP ngrok tunnel to the SSH server
connection_string = ngrok.connect("22", "tcp").public_url

ssh_url, port = connection_string.strip("tcp://").split(":")
print(f" * ngrok tunnel available, access with `ssh root@{ssh_url} -p{port}`")
app = Flask(__name__)
port = "5000"

# 替换成你的 LINE Bot 的 Access Token 和 Channel Secret
access_token = "u2jc0ieZWiYRP0mm9x4Ii3H4aqsd3dkUFZUkuho9VVRcHO88rY1cMeMRuF2V/vr+tKgRWVmZtmXTBAnzNLoU+MVtOC1aVHdbIY9TUuiMcViMxnjGeqp8dcd+qTLvMIyF9CQyL/Vng7B+Fj21SV/k5QdB04t89/1O/w1cDnyilFU="
secret = "c53bec8d8125fd46765777e813083df7"
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(f" * ngrok tunnel \"{public_url}\" -> \"https://127.0.0.1:{port}\" ")

#line_bot_api.push_message('Ub48bdf60f274e6ccc6490866eae11089',TextSendMessage(text='機器人已啟用'))
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

#查看菜單
def view_menu(msg,reply_token,hint):
    if(msg.isdigit() == False or 7<int(msg) or int(msg)<0):
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的數字\n'+hint))
        print("error")
    elif(int(msg)==0):
        line_bot_api.reply_message(reply_token,TextMessage(text='取消成功, 請使用圖文選單取得幫助!'))
        Msg_package.flag=-1
        print("success")
    else:
        image_message = db_cmd.view_menu(msg)
        menu=ImageSendMessage(
            original_content_url=image_message,
            preview_image_url=image_message
        )
        line_bot_api.reply_message(reply_token,menu)
        print(msg)
        Msg_package.flag=-1

#立即點餐
def order_now(msg,reply_token,hint,user_id):
    msg2 = [line.split(',') for line in msg.split('\n')]
    msg3 = [item for sublist in msg2 for item in sublist]
    msg4 = [line.split('，') for line in msg3]
    msg_clone = [item for sublist in msg4 for item in sublist]
    store=['早安美廣', '傳香飯糰', '八方雲集', '宜廷小吃', '琪美食堂', '美廣鮮果吧', '自助餐']
    if(msg_clone[0] not in store):
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的店家名稱或是輸入完店家空行\n'+hint))
        print("error")
    else:
        for i in range(2, len(msg_clone), 2):
            if not msg_clone[i].isdigit():
                line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的數量(數字)\n'+hint))
                print("error")
        order_id=db_cmd.order_now(msg,Msg_package.user_id)
        Msg_package.now_id=order_id
        line_bot_api.reply_message(reply_token,TextMessage(text='訂單完成\n你的訂單id是'+str(order_id)))
        Msg_package.flag=-1
        thread = threading.Thread(target=order_finish_or_not, args=(Msg_package.user_id,))
        thread.daemon = True
        thread.start()
        
#查看訂單
def view_order(msg,reply_token,hint):
    if not msg.isdigit():
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的訂單id\n'+hint))
    else:
        message = db_cmd.view_order(msg)
        if message == '沒有此訂單，請確認訂單id是否有打對\n':
            line_bot_api.reply_message(reply_token,TextMessage(text=message+hint))
        else:
            line_bot_api.reply_message(reply_token,TextMessage(text=message))
            Msg_package.flag=-1

#取消訂單      
def delete_order(msg,time,reply_token,hint):
    if not msg.isdigit():
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的訂單id\n'+hint))
    else:
        message = db_cmd.delete_order(msg,time)
        line_bot_api.reply_message(reply_token,TextMessage(text=message))
        Msg_package.flag=-1
        
#訂單是否完成
def order_finish_or_not(user_id):
    while(Msg_package.now_id != 0):
        order_status = db_cmd.check_order_finish(Msg_package.now_id)
        if(order_status == 1):
            line_bot_api.push_message(user_id, messages=[TextSendMessage(text="你的訂單"+Msg_package.now_id+"已經完成\n請前往學餐取餐點")])
            Msg_package.now_id=0
        sleep(2)    
            

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_token = event.reply_token
    Msg_package.user_id = event.source.user_id
    #case "營業時間"
    if(message_text=="營業時間" or Msg_package.flag==1):
        line_bot_api.reply_message(reply_token,TextMessage(text=db_cmd.run_time()))
        Msg_package.flag=-1
    #case "查看菜單"
    if(message_text=="查看菜單" or Msg_package.flag==2):
        hint = "輸入數字來選擇想要查看的店家菜單：\n0. 取消\n1. 早安美廣\n2. 傳香飯糰\n3. 八方雲集\n4. 宜廷小吃\n5. 琪美食堂\n6. 美廣鮮果吧\n7. 自助餐"
        if(Msg_package.flag==-1):
            print("查看菜單")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=2
        else:
            Msg_package.msg=message_text
            view_menu(Msg_package.msg,reply_token,hint)
    #case "立即點餐"
    if(message_text=="立即點餐"or Msg_package.flag==3):
        hint='輸入格式如下:\n店家名稱\n商品名稱,數量'
        if(Msg_package.flag==-1):
            print("立即點餐")
            if(Msg_package.now_id != 0):
                line_bot_api.reply_message(reply_token, TextSendMessage(text='你先前的訂單尚未完成'))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
                Msg_package.flag=3
        else:
            Msg_package.msg=message_text
            order_now(Msg_package.msg,reply_token,hint,Msg_package.user_id)
    #case "查看訂單"
    if(message_text=="查看訂單"or Msg_package.flag==4):
        hint='請給我你的訂單id'
        if(Msg_package.flag==-1):
            print("查看訂單")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=4
        else:
            Msg_package.msg=message_text
            view_order(Msg_package.msg,reply_token,hint)
    #case "取消訂單"
    if(message_text=="取消訂單"or Msg_package.flag==5):
        hint='請給我你的訂單id'
        if(Msg_package.flag==-1):
            print("取消訂單")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=5
        else:
            Msg_package.msg=message_text
            timestamp = event.timestamp
            print(timestamp)
            delete_order(Msg_package.msg,timestamp,reply_token,hint)
    #case "優惠資訊":
    if(message_text=="優惠資訊"):
        line_bot_api.reply_message(reply_token, TextSendMessage(text="活動規則:\n1.消費每五十元集一點，消費時一點可抵一元。\n2.花費點數參加抽獎\n抽獎方式為隨機骰0~100,如果>60點則獲得花費點數*(1+(骰的數字-60))/100\n如果<=60則抽獎失敗\n輸入 我要抽獎 開始抽獎"))
    #case "抽獎系統":
    if(message_text=="我要抽獎"or Msg_package.flag==6):
        if(Msg_package.flag==-1):
            line_bot_api.reply_message(reply_token, TextSendMessage(text='花費點數參加抽獎，獲得點數為花費的點數加上抽出的數字\n請輸入要花費的點數(請輸入數字)'))
            Msg_package.flag=6
        else:
            msg=message_text
            Msg_package.user_id=event.source.user_id
            if msg.isdigit():
                if db_cmd.spend_point(Msg_package.user_id,int(msg)):
                    rate=db_cmd.lottery(Msg_package.user_id,int(msg))
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='骰到的數字為: '+str(rate[0])+'\n總共獲得: '+str(rate[1])+'點'))
                    Msg_package.flag=-1
                else:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='點數不足'))
                    Msg_package.flag=-1
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(text='你輸入的不是數字'))
                Msg_package.flag=-1
    #case "會員資訊":
    if(message_text=="會員資訊"):
        member_information=db_cmd.member_information(Msg_package.user_id)
        line_bot_api.reply_message(reply_token, TextSendMessage(text=member_information))

#加入好友後建立會員資料進資料庫
@handler.add(FollowEvent)
def handle_follow(event):
    user_id=event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    db_cmd.add_member(profile.user_id,profile.display_name)

#刪除好友後資料庫刪除會員資料
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id=event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    db_cmd.delete_member(profile.user_id)

#啟動服務
if __name__ == "__main__":
    app.run()