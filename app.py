from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import traceback
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 呼叫 LLM 的 API 端點
llm_api_url = os.getenv('LLM_CHAT_API_URL')
api_token = os.getenv('LLM_CHAT_API_URL_TOKEN')

def answer_question(question):
    payload = {
        'token': api_token,
        'query': question
    }
    try:
        # 呼叫 LLM API
        response = requests.post(llm_api_url, data=payload)
        response_data = response.json()
        # 從回應中取得結果
        if response_data.get("status") == "OK":
            return response_data.get("result")
        else:
            return "API 回應錯誤，請稍後再試。"
    except Exception as e:
        print(traceback.format_exc())
        return "呼叫 LLM 服務時發生錯誤。"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        # 使用 LLM API 獲取回答
        GPT_answer = answer_question(msg)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except Exception as e:
        print(traceback.format_exc())
        error_message = '發生錯誤，請檢查日誌以了解詳情，請聯繫客服。'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(error_message))

@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import traceback
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 呼叫 LLM 的 API 端點
llm_api_url = os.getenv('LLM_CHAT_API_URL')
api_token = os.getenv('LLM_CHAT_API_URL_TOKEN')

def answer_question(question):
    payload = {
        'token': api_token,
        'query': question
    }
    try:
        # 呼叫 LLM API
        response = requests.post(llm_api_url, data=payload)
        response_data = response.json()
        # 從回應中取得結果
        if response_data.get("status") == "OK":
            return response_data.get("result")
        else:
            return "API 回應錯誤，請稍後再試。"
    except Exception as e:
        print(traceback.format_exc())
        return "呼叫 LLM 服務時發生錯誤。"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        # 使用 LLM API 獲取回答
        GPT_answer = answer_question(msg)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except Exception as e:
        print(traceback.format_exc())
        error_message = '發生錯誤，請檢查日誌以了解詳情。'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(error_message))

@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
