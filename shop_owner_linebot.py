import threading
from time import sleep
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
db_settings_file=open('C:\\Users\\USER\\Desktop\\school_menu_discount\\db_setting.json','r')
db_settings=json.load(db_settings_file)
ngrok_path = 'C:\\Users\\USER\\Desktop\\school_menu_discount\\ngrok.exe'
conf.get_default().ngrok_path=ngrok_path
conf.get_default().auth_token = '2gGEvboQS0QRUwcn7YsRTHfhXJT_6zC4BD7uerBsrxjnz6HJU'
#conf.get_default().auth_token = getpass.getpass(auth)

class Msg_package:
    count = 0
    number = ''  # 保存廠商編號
    msg='' #保存使用者訊息
    flag=-1 #判斷是否被占用

# Open a TCP ngrok tunnel to the SSH server
connection_string = ngrok.connect("22", "tcp").public_url

ssh_url, port = connection_string.strip("tcp://").split(":")
print(f" * ngrok tunnel available, access with `ssh root@{ssh_url} -p{port}`")
app = Flask(__name__)
port = "5001"

# 替换成你的 LINE Bot 的 Access Token 和 Channel Secret
access_token = "ycCdDfOIP0RTCcX3wChO+9glfcA56TaLmvX6e77stOqBejZumBpBsbTnDwYe+S9sth1ZErzHL/C0I21wCfgvbS/4NUIZW9U+QWAvNCPpQvJIEip3ecKJfQ6anez4WCJd6KYtIBTswswTyltckFpYVQdB04t89/1O/w1cDnyilFU="
secret = "f9276d118079f2082f30e3199a1ad494"
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
#確認是否有新訂單
def check_new_order(shop_id, user_id):
    if Msg_package.number in ['1', '2', '3', '4', '5', '6', '7']:
        while True:
            current_count = db_cmd.check_order(shop_id)
            if int(current_count) > Msg_package.count:
                Msg_package.count = int(current_count)
                order_id = db_cmd.get_order_id(shop_id)
                message = db_cmd.view_order(order_id)
                line_bot_api.push_message(user_id, messages=[TextSendMessage(text="你有一筆新的訂單\n" + message)])
            sleep(2)
            
# 完成訂單            
def finish_order(order_id, reply_token, hint):
    if not order_id.isdigit():
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的訂單id\n'+hint))
    else:
        db_cmd.finish_order(order_id)
        line_bot_api.reply_message(reply_token,TextMessage(text='訂單完成'))
        Msg_package.flag = -1
        
#查看訂單        
def check_order(order_id, reply_token, hint):
    if not order_id.isdigit():
        line_bot_api.reply_message(reply_token,TextMessage(text='請輸入正確的訂單id'+hint))
    else:
        message = db_cmd.view_order(order_id)
        if message == '沒有此訂單，請確認訂單id是否有打對\n':
            line_bot_api.reply_message(reply_token,TextMessage(text=message+hint))
        else:
            line_bot_api.reply_message(reply_token,TextMessage(text=message))
            Msg_package.flag=-1
            
#完成付款
def finish_pay(order_id, user_id, reply_token, hint):
    if not order_id.isdigit():
        line_bot_api.reply_message(reply_token, TextMessage(text='請輸入正確的訂單id'+hint))
    else:
        message = db_cmd.order_pay(order_id, user_id)
        if message == '沒有此訂單，請確認訂單id是否有打對\n':
            line_bot_api.reply_message(reply_token,TextMessage(text=message+hint))
        else:
            line_bot_api.reply_message(reply_token,TextMessage(text="付款完成"))
            Msg_package.flag=-1
        

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_token = event.reply_token
    user_id = event.source.user_id
    #case廠商登入
    if (message_text == "廠商登入" or Msg_package.flag == 1):
        hint = "請輸入廠商編號以登入帳號"
        if (Msg_package.flag == -1):
            print("廠商登入")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag = 1
        else:
            Msg_package.number = message_text
            Msg_package.count = db_cmd.check_order(Msg_package.number)
            line_bot_api.reply_message(reply_token, TextSendMessage(text="登入成功"))
            Msg_package.flag = -1
            thread = threading.Thread(target=check_new_order, args=(Msg_package.number, user_id))
            thread.daemon = True
            thread.start()
    #case查看訂單        
    if (message_text == "查看訂單" or Msg_package.flag == 2):
        hint1 = "這些是你尚未完成的的訂單編號\n"
        hint3 = "\n請輸入編號來選擇想確認的訂單"
        if(Msg_package.flag == -1):
            print("查看訂單")
            hint2 = db_cmd.unfinish_order(Msg_package.number)
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint1+hint2+hint3))
            Msg_package.flag=2
        else:
            Msg_package.msg = message_text
            check_order(Msg_package.msg, reply_token, hint3)

    #case訂單完成
    if (message_text == "訂單完成" or Msg_package.flag == 3):
        hint = "請輸入完成的訂單編號"
        if (Msg_package.flag == -1):
            print("訂單完成")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=3
        else:
            Msg_package.msg = message_text
            finish_order(Msg_package.msg,reply_token,hint)
            
    #case付款完成
    if (message_text == "付款完成" or Msg_package.flag == 4):
        hint = "請輸入完成付款的訂單編號"
        if (Msg_package.flag==-1):
            print("付款完成")
            line_bot_api.reply_message(reply_token, TextSendMessage(text=hint))
            Msg_package.flag=4
        else:
            Msg_package.msg = message_text
            finish_pay(Msg_package.msg, user_id, reply_token, hint)
# 啟動服務
if __name__ == "__main__":
    app.run(port=5001)
