from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def first(answers: list):
    markup = InlineKeyboardMarkup()
    for number, answer in enumerate(answers, start=0):
        markup.add(InlineKeyboardButton(text=str(answer), callback_data='q1a_' + str(number)))
    return markup

def second(answers: list):
    markup = InlineKeyboardMarkup()
    for number, answer in enumerate(answers, start=0):
        markup.add(InlineKeyboardButton(text=str(answer), callback_data='q2a_' + str(number)))
    return markup

def third(answers: list):
    markup = InlineKeyboardMarkup()
    for number, answer in enumerate(answers, start=0):
        markup.add(InlineKeyboardButton(text=str(answer), callback_data='q3a_' + str(number)))
    return markup

