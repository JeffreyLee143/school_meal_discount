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
import json
db_settings_file=open('src\db_setting.json','r')
db_settings=json.load(db_settings_file)
ngrok_path = 'src\\ngrok.exe'
conf.get_default().ngrok_path=ngrok_path
conf.get_default().auth_token = '2fzU7K2oDcw4rNQ4i8JMEoZrzpV_28yEF9t59wiXrMQULEBA7'
#conf.get_default().auth_token = getpass.getpass(auth)

class Msg_package:
    msg='' #保存使用者訊息
    flag=-1 #判斷是否被占用

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
def order_now(msg,reply_token,hint):
    db_cmd.order_now(msg)
    Msg_package.flag=-1

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_token = event.reply_token
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
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=3
        else:
            Msg_package.msg=message_text
            order_now(Msg_package.msg,reply_token,hint)
    #case "優惠資訊":
    if(message_text=="優惠資訊"):
        print("優惠資訊")

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