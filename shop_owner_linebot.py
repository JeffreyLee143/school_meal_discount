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

def check_order(shop_id, user_id):
    if Msg_package.number in ['1', '2', '3', '4', '5', '6', '7']:
        while True:
            current_count = db_cmd.check_order(shop_id)
            if int(current_count) > Msg_package.count:
                Msg_package.count = int(current_count)
                order_id = db_cmd.get_order_id(shop_id)
                message = db_cmd.view_order(order_id)
                line_bot_api.push_message(user_id, messages=[TextSendMessage(text="你有一筆新的訂單\n" + message)])
            sleep(2)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_token = event.reply_token
    user_id = event.source.user_id
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
            thread = threading.Thread(target=check_order, args=(Msg_package.number, user_id))
            thread.daemon = True
            thread.start()

# 启动服务
if __name__ == "__main__":
    app.run(port=5001)