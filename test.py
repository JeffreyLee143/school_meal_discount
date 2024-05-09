from flask import Flask, request, abort
from pyngrok import ngrok, conf
from linebot.webhook import WebhookHandler
from linebot import LineBotApi
from linebot.v3.exceptions import InvalidSignatureError
from linebot.models import *
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img
import os
import getpass
import db_cmd
import csv
import pymysql
import json
db_settings_file=open('src\db_setting.json','r')
db_settings=json.load(db_settings_file)
ngrok_path = 'src\\ngrok.exe'
conf.get_default().ngrok_path=ngrok_path
conf.get_default().auth_token = '2fzU7K2oDcw4rNQ4i8JMEoZrzpV_28yEF9t59wiXrMQULEBA7'
#conf.get_default().auth_token = getpass.getpass(auth)

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

def member_informaton():
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        message_text = event.message.text
        msg=message_text.split(',')
        if(len(msg)!=3):
            line_bot_api.reply_message(event.reply_token,TextMessage(text='請輸入正確的資訊'))
            handle_message(event)
        db_cmd.add_member(msg[0],msg[1],msg[2])

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_token = event.reply_token
    # 這裡是點餐系統的處理邏輯
    if(message_text=="營業時間"):
            line_bot_api.reply_message(event.reply_token,TextMessage(text=db_cmd.run_time()))
        #case "立即點餐":
        #case "查看菜單":
        #case "優惠資訊":
            
    #if msg[0] == '新增菜單':
    #    member_informaton()
        #db_cmd.add_member(msg[1],msg[2],msg[3])

if __name__ == "__main__":
    app.run()