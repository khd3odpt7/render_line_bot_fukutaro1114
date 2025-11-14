from flask import Flask, request, abort
import os
import logging

from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging.models import TextMessage

app = Flask(__name__)

# 環境変数からキーを取得
channel_secret = os.getenv("CHANNEL_SECRET")
channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")

if not channel_secret or not channel_access_token:
    raise ValueError("CHANNEL_SECRET or CHANNEL_ACCESS_TOKEN is not set.")

# v3用の設定
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        logging.exception("Webhook error")
        return "Error", 200

    return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    print(f"userId: {user_id}")

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=[TextMessage(text="こんにちは！")]
        )