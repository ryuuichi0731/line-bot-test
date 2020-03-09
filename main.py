from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import os
import json

#アクセスキーの取得
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.type == "message":
        if (event.message.text == "施設を選択"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='メッセージを送信しました。一つしたにあるメッセージをタップするか、トーク画面下にある選択ボタンからお選びください。'),
                    
                    {
                      "type": "template",
                      "altText": "this is a carousel template",
                      "template": {
                        "type": "carousel",
                        "actions": [],
                        "columns": [
                          {
                            "thumbnailImageUrl": "https://www.aeon-jreit.co.jp/file/portfolio-f42a862f3c3b544b4e48580a3f2c1f0702b4c23e.jpg?timestamp=1543536000025",
                            "title": "①",
                            "text": "ショッピングセンター",
                            "actions": [
                              {
                                "type": "message",
                                "label": "施設①",
                                "text": "アクション 01"
                              }
                            ]
                          },
                          {
                            "thumbnailImageUrl": "https://pbs.twimg.com/media/CuJU08bUAAAjjpA.jpg",
                            "title": "②",
                            "text": "けいはんなオープンイノベーションセンター",
                            "actions": [
                              {
                                "type": "message",
                                "label": "施設②",
                                "text": "アクション 02"
                              }
                            ]
                          },
                          {
                            "thumbnailImageUrl": "https://lighthouse1922.sakura.ne.jp/nlhwww/iccb/wp-content/uploads/parts/about.jpg",
                            "title": "③",
                            "text": "文化センター",
                            "actions": [
                              {
                                "type": "message",
                                "label": "施設③",
                                "text": "アクション 03"
                              }
                            ]
                          }
                        ]
                      }
                    }
                ] 
            )
                
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
