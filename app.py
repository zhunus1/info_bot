#t.me/Margo_Kriminskaya_bot
import config
import time
import asyncio

import telegram
import requests
from flask import Flask, request

app = Flask(__name__)
global bot 
bot = telegram.Bot(token=config.token)

#Need API for Прогревы и Напоминания. TEXT

@app.route('/{}'.format(config.token), methods=['POST'])
async def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    if update.message.from_user.first_name:
        username = update.message.from_user.first_name
    else:
        username = update.message.from_user.last_name

    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == "/start":
        bot_welcome = """
        Привет, %s! 
        Я рада, что ты с нами! Добро пожаловать на самый эффективный БЕСПЛАТНЫЙ 3-х дневный тренинг ,который помогает понять почему одни успешно зарабатывают миллионы, а другие стоят на месте ? Почему история долгов и кредитов не заканчивается в твоей жизни ? 
        Так же я подготовила 7 конкретных шагов для изменения твоих финансов в течении 30 дней!

        Поэтому, ставь напоминание на 11 декабря ,чтобы не пропустить.

        Если ты подойдешь к прохождению тренинга ответственно, посетишь все три дня и будешь выполнять все задания, то заметишь положительные перемены в течении 2х дней.

        Я верю в каждого из вас, даже если ты в себя не веришь пока ещё - помни мои слова 🙌
        """ % username
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
        
        traning_description = """
        🔥Темы , которые будут раскрыты на тренинге:

        ◽️Долги и кредиты 
        ◽️Почему одни успешно зарабатывают, а другие стоят на месте ?
        ◽️Не получается- много обучаюсь , но нет результата
        ◽️Секрет успеха от миллионера 
        ◽️7 конкретных шагов для изменения жизни за 30 дней
        ◽️ Что мешает сделать результат и сдвинуться с места?
        ◽️Как найти свою нишу и понять чем заниматься ?
        ◽️Презентация нового курса

        Не пропусти - 11 декабря мы начинаем 🔥
        """
        await asyncio.sleep(7)
        bot.sendMessage(chat_id=chat_id, text=traning_description, reply_to_message_id=msg_id)
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL="https://ea62-2-72-253-12.ngrok.io/", HOOK=config.token), allowed_updates=[])
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)