import config
import asyncio
import requests
import telegram
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db import get_db
from db import close_db


bp = Blueprint('bot', __name__, url_prefix='/bot')
bot = telegram.Bot(token=config.token)


@bp.route('/notify', methods=['POST'])
async def notify_all():
    db = get_db()

    cur = g.db.cursor()
    cur.execute("SELECT * FROM user")
    chats = cur.fetchall()
    cur.close()
    for chat in chats:
        print(chat['chat_id'])
        try:
            key = request.headers.get('x-api-key')
            if key == 'Behappy7+':
                notify_text = request.form.get('text')
                try:
                    bot.sendMessage(chat_id=chat['chat_id'], text=notify_text)
                except:
                    print('Bot was blocked by the user')
            else:
                return "Bad request", 400
        except:
            return "Bad request", 400
        await asyncio.sleep(0.5)
    close_db()
    return "ok"

@bp.route('/{}'.format(config.token), methods=['POST'])
async def respond():

    db = get_db()

    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.my_chat_member:
        return 'ok'
    
    chat_id = update.message.chat.id
    msg_id = update.message.message_id 
    
    if update.message.from_user.first_name:
        username = update.message.from_user.first_name
    else:
        username = update.message.from_user.last_name
    users = db.execute('SELECT * FROM user')

    cur = g.db.cursor()
    cur.execute("""SELECT chat_id
                          ,username
                   FROM user
                   WHERE chat_id=?
                       OR username=?""",
                (chat_id, username))

    result = cur.fetchone()
    cur.close()
    if not result:
        db.execute("INSERT INTO user (username, chat_id) VALUES (?, ?)", (username, chat_id),)
        db.commit()
    
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == "/start":
        try:
            bot_welcome = '''Привет, %s 👋
            \nЯ рада, что ты с нами! Добро пожаловать на самый эффективный БЕСПЛАТНЫЙ 3-х дневный тренинг, который помогает понять почему одни успешно зарабатывают миллионы, а другие стоят на месте?
            \nПочему история долгов и кредитов не заканчивается в твоей жизни?
            \nТак же я подготовила 7 КОНКРЕТНЫХ ШАГОВ для изменения твоих финансов в течении 30 ДНЕЙ!
            \nПоэтому, ставь напоминание на 11 декабря ,чтобы не пропустить⏰
            \nЕсли ты подойдешь к прохождению тренинга ответственно, посетишь все три дня и будешь выполнять все задания, то заметишь положительные перемены в течении 2х дней🔥
            \n❤️Я верю в каждого из вас, даже если вы в себя не верите пока ещё - помни мои слова 🙌
            ''' % username
            bot.sendPhoto(chat_id=chat_id, photo='AgACAgIAAxkDAAIBZ2G0HIpMpQ68DhGbAm2XpydapYkaAAJevDEbeDagSRXlXKhnlGYUAQADAgADcwADIwQ', caption=bot_welcome)
            
            traning_description = '''🔥Темы, которые будут раскрыты на тренинге:
            \n▪️Долги и кредиты\n▪️Почему одни успешно зарабатывают, а другие стоят на месте ?\n▪️Не получается - много обучаюсь, но нет результата!\n▪️Секрет успеха от миллионера 🤫\n▪️7 конкретных шагов для изменения жизни за 30 дней!\n▪️Что мешает сделать результат и сдвинуться с места?\n▪️Как найти свою нишу и понять чем заниматься?\n▪️🎥 Презентация нового курса!

            \nНе пропусти - 11 декабря мы начинаем! 🔥
            '''
            await asyncio.sleep(7)
            bot.sendPhoto(chat_id=chat_id, photo='AgACAgIAAxkDAAIBaWG0HPmT236-pvXt0wlcy-IUczhkAAI2tTEbzZGgSTdnbS8uTPucAQADAgADcwADIwQ', caption=traning_description)
        except:
            print('Bot was blocked by the user')
    close_db()
    return 'ok'

@bp.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL="https://bot.info-platform.com/bot/", HOOK=config.token), allowed_updates=[])
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"