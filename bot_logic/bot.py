from aiogram.filters import CommandStart
from aiogram import types
from aiogram.utils.markdown import hbold
from .loader import dp


@dp.message(CommandStart()) #регистрирует этот обработчик для команды /start
async def cmd_start(message: types.Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')

@dp.message()
async def echo_handler(message:types.Message) -> None:
    try:
        await message.send_copy(chat_id = message.chat.id)
    except TypeError:
        await message.answer("Техничесвие шоколадки!")