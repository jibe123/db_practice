from config import ADMIN_USER_ID, TOKEN
import telebot
import datetime as dt
from models import TGUser, Note
import db

from telebot.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
ReplyKeyboardMarkup,
KeyboardButton
)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_text = f"""
Добро пожаловать в менеджер заметок!
Пожалуйста, выберите действие ниже:"""
    id_of_user = str(message.from_user.id)
    user_name = message.from_user.username
    query = TGUser.select().where(TGUser.userid_tg == id_of_user)
    if query.exists():
        pass
    else:
        TGUser.create(userid_tg=id_of_user, username=user_name)
    bot.send_sticker(message.chat.id,
                     sticker="CAACAgIAAxkBAAEFpxxjBQQH1ZSAIMeORVVr80igIHx8ZgACSxgAAhhOaUnuLzvXuof7TikE")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup_adder(), parse_mode="HTML")


def markup_adder():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    new_note = InlineKeyboardButton("Добавить заметку", callback_data="new_note")
    show_notes = InlineKeyboardButton("Просмотреть все заметки", callback_data="show_notes")
    markup.add(new_note, show_notes)
    return markup


@bot.callback_query_handler(func=lambda call: call.data == "new_note")
def new_note(call):
    message = call.message
    new_note_text = f"""
Пожалуйста, введите текст своей заметки!"""
    bot.send_message(message.chat.id, new_note_text)
    bot.register_next_step_handler(message, callback=submit_note)


def submit_note(message):
    user_note = message.text
    id_of_user = str(message.from_user.id)
    date_raw = message.date
    date = dt.datetime.utcfromtimestamp(date_raw).strftime("%Y-%m-%d")
    Note.create(userid=id_of_user, note=user_note, date=date)
    accept_text = f"""
    Спасибо, ваша заметка записана!"""
    bot.send_message(message.chat.id, accept_text, reply_markup=markup_adder())


@bot.callback_query_handler(func=lambda call: call.data == "show_notes")
def show_notes(call):
    message = call.message
    id_of_user = str(call.from_user.id)
    query = Note.select().where(Note.userid == id_of_user)
    notes_list = [item for item in query]
    for item in notes_list:
        text = f"Дата заметки: {item.date}\nТекст: {item.note}"
        bot.send_message(message.chat.id, text)
    final_text = f"""
        Это были все ваши заметки!"""
    bot.send_message(message.chat.id, final_text, reply_markup=markup_adder())


bot.infinity_polling()