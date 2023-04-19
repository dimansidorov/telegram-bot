import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
from aiogram import F

from config import API_TOKEN


bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

users: dict = {}

START_INT: int = 1
END_INT: int = 100

ATTEMPTS: int = 5


def get_random_number() -> int:
    return random.randint(START_INT, END_INT)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }
    print(users)
    await message.answer('Привет!\nЭто бот-угадайка!\n'
                         'Получить список доступных комманд и\n'
                         'узнать правила - команда /help')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего сыгранно игр: {users[message.from_user.id]["total_games"]}\n'
                         f'Колличество побед: {users[message.from_user.id]["wins"]}')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(f'Игра окончена')
    else:
        await message.answer(f'А мы итак с вами не играем. Есть желание сыграть?')


@dp.message(Text(text=['да', 'хочу', 'буду', 'давай', 'игра', 'играем', 'игра', 'сыграем'], ignore_case=True))
async def process_positive_answer(message: Message):
    try:
        if not users[message.from_user.id]['in_game']:
            await message.answer(f'Я загадал число от {START_INT} до {END_INT}. У тебя {ATTEMPTS} попыток, попробуй угадать')
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['secret_number'] = get_random_number()
            users[message.from_user.id]['attempts'] = ATTEMPTS
        else:
            await message.answer(f'В данный момент я реагирую только на комманды /cancel и /stat')
    except KeyError:
        number = get_random_number()
        users[message.from_user.id] = {
            'in_game': True,
            'secret_number': number,
            'attempts': ATTEMPTS,
            'total_games': 0,
            'wins': 0
        }
        await message.answer(f'Я загадал число от {START_INT} до {END_INT}. У тебя {ATTEMPTS} попыток, попробуй угадать')


@dp.message(Text(text=['не', 'не хочу', 'не буду', 'нет', 'игра', 'играем', 'игра', 'сыграем'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(f'Очень жаль. Дайте мне знать, если захотите играть')
    else:
        await message.answer(f'Вы уже играете. Если вы хотите остановить игру - воспользуйтесь командой /cancel')


@dp.message(lambda x: x.text and x.text.isdigit() and START_INT <= int(x.text) <= END_INT)
async def process_number_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                                 f'сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы не играем. Хочешь сыграть?')


@dp.message()
async def process_other_text_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Я умею только загадывать числа. Хочешь сыграть?')
    else:
        await message.answer(f'Мы сейчас играем. Я ожидаю от тебя число от {START_INT} до {END_INT}')

if __name__ == '__main__':
    dp.run_polling(bot)
