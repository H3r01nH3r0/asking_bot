from db import Database
from aiogram import Bot, Dispatcher, types, executor, filters
import keyboards as nav
from time import sleep

db = Database('database.db')
bot = Bot(token="1900305542:AAHjQjTgBu8LvoNb69FpxOdnnXFKWIuNKTA", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
admin_id = 5047191962
owners_filter = filters.IDFilter(user_id=str(admin_id))

def get_answers(question_id):
    answers = db.get_answers(question_id).split('_')
    return answers

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message) -> None:
    username = message.from_user.username
    user_id = message.from_user.id
    if db.check_user(user_id):
        await bot.send_photo(user_id, open('photo.jpg', 'rb'), caption='хуй')
        await bot.send_message(user_id, text='Коллеги, добрый день!\nПройдите пожалуйста этот небольшой опрос!')
        await bot.send_message(user_id, text=db.get_question(1), reply_markup=nav.first(get_answers(1)))
    else:
        db.add_user(user_id, username)
        await bot.send_photo(user_id, open('photo.jpg', 'rb'), caption='хуй')
        await bot.send_message(user_id, text='Коллеги, добрый день!\nПройдите пожалуйста этот небольшой опрос!')
        await bot.send_message(user_id, text=f'<b>Вопрос №1</b>\n\n{db.get_question(1)}', reply_markup=nav.first(get_answers(1)))

@dp.message_handler(commands=["stat"])
async def owners_users_command_handler(message: types.Message) -> None:
    users = db.user_count()
    count = db.get_answer_count()
    count1 = db.get_answer_count_1()
    count2 = db.get_answer_count_2()
    count3 = db.get_answer_count_3()
    await message.answer(text=f'<b>Статистика</b>\n\nВсего пользователей приняло участия в опросе: <b>{users}</b>\n'
                              f'Всего пользовали ответили на <b>{count}</b> вопрос(ов)\n'
                              f'На первый вопрос ответили <b>{count1}</b> пользователей\n'
                              f'На второй вопрос ответили <b>{count2}</b> пользователей\n'
                              f'На третий вопрос ответили <b>{count3}</b> пользователей\n')


@dp.message_handler(content_types = ['location'])
async def bot_message(message: types.Location, ):
    print(message.location)



@dp.callback_query_handler(state="*")
async def callback_query_handler(callback_query: types.CallbackQuery) -> None:
    data = callback_query.data.split('_')
    user_id = callback_query.from_user.id
    if data[0] == 'q1a':
        answer = get_answers(1)[int(data[1])]
        db.set_answer(user_id, 1, answer)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(user_id, text=f'<b>Вопрос №2</b>\n\n{db.get_question(2)}', reply_markup=nav.second(get_answers(2)))
    elif data[0] == 'q2a':
        answer = get_answers(2)[int(data[1])]
        db.set_answer(user_id, 2, answer)
        print('ты пидор')
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(user_id, text=f'<b>Вопрос №3</b>\n\n{db.get_question(1)}', reply_markup=nav.third(get_answers(3)))
    elif data[0] == 'q3a':
        answer = get_answers(3)[int(data[1])]
        db.set_answer(user_id, 3, answer)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(user_id, text='Коллеги, спасибо!')
        await bot.send_message(admin_id, text=f'Пользователь @{callback_query.from_user.username} завершил участие в опросе\n\n'
                                              f'<b>Ответы</b>\n\n<b>Вопрос №1</b>\n\n{db.get_user_answer(user_id, 1)}\n\n'
                                              f'<b>Вопрос №2</b>\n\n{db.get_user_answer(user_id, 2)}\n\n'
                                              f'<b>Вопрос №3</b>\n\n{db.get_user_answer(user_id, 3)}\n\n')


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)