from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from config.config import TOKEN


bot = Bot(token=TOKEN)
bot.parse_mode = 'HTML'

dp = Dispatcher()