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
                    TextSendMessage(
                        text='下に表示されている施設名が書かれた、ボタンをタップして選択してください。',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label="ショッピングセンター", text="Shopping center")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="科学技術センター", text="Science & Technology center")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="情報文化センター", text="Media & Communication center")
                        ),
                    ])))
       

    if event.type == "message":
        if (event.message.text == "Shopping center"):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='下に表示されている目的地が書かれた、ボタンをタップして選択してください。',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label="１階 トイレ", text="floor1 Toilet")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="レストラン", text="Restaurant")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="エントランス", text="Entrance")
                        ),
                    ])))
           
    if event.type == "message":
        if (event.message.text == "Science & Technology center"):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='下に表示されている目的地が書かれた、ボタンをタップして選択してください。',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label="多目的 トイレ", text="Multipurpose　Toilet")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="メインホール", text="Main Hall")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="セミナールーム", text="Seminar Room")
                        ),
                    ])))
    if event.type == "message":
        if (event.message.text == "Media & Communication center"):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='下に表示されている目的地が書かれた、ボタンをタップして選択してください。',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label="フロア３ トイレ", text="floor3 Toilet")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="エレベーター", text="Elevator")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="会議室", text="Conference Room")
                        ),
                    ])))
        else:
            line_bot_api.reply_message( 
                event.reply_token,    
                TextSendMessage(        
                    text='返答内容を理解することができませんでした。大変申し訳ありませんが、別の回答をお試しください。')
            )
    

    if event.type == "message":
        if (event.message.text == "floor1 Toilet") or (event.message.text == "Restaurant") or (event.message.text == "Entrance") or (event.message.text == "Multipurpose　Toilet") or (event.message.text == "Main Hall") or (event.message.text == "Seminar Room") or (event.message.text == "floor3 Toilet") or (event.message.text == "Elevator") or (event.message.text == "Conference Room"):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='選択した目的地までの案内を開始してよろしいですか。下のメッセージから選択してください。',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label="案内をはじめる", text="navigation_start")
                        ),
                                QuickReplyButton(
                                    action=MessageAction(label="案内をキャンセル", text="navigation_cancel")
                        ),
                    ])))
    if event.type == "message":
        if (event.message.text == "navigation_start"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='案内を開始します。')
            )
    if event.type == "message":
        if (event.message.text == "navigation_cancel"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='案内をキャンセルしました。')
            )
        else:
            line_bot_api.reply_message( 
                event.reply_token,    
                TextSendMessage(        
                    text='返答内容を理解することができませんでした。大変申し訳ありませんが、別の回答をお試しください。')
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
