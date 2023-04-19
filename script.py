from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F

from config import API_TOKEN



bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


async def process_start_command(message: Message):
    await message.answer('Привет!')


async def process_help_command(message: Message):
    await message.answer('Напиши мне что угодно, а я буду отвечать тебе тем же')


async def send_echo(message: Message):
    try:
        
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')


dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_echo)


if __name__ == '__main__':
    dp.run_polling(bot)