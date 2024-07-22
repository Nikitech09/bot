from aiogram.filters import CommandStart, Command
from aiogram import types,F
from aiogram.utils.markdown import hbold
from .loader import dp,TOKEN
import requests
import random

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('

users = {}

#Количество попыток, доступных пользователю в игре
ATTEMPTS = 5

def get_random_number()-> int:
    return random.randint(1,100)

@dp.message(CommandStart()) #регистрирует этот обработчик для команды /start
async def cmd_start(message: types.Message) -> None:
    await message.answer('Привет!\nдавайте сыграем в игру "Угадай число"? \n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game':False,
            'secret_number':None,
            'attempts':None,
            'total_games':0,
            'wins':0   
        }

@dp.message(Command(commands='help'))
async def process_help_command(message: types.Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )
    
@dp.message(Command(commands='/stat'))
async def process_stat_command(message: types.Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: types.Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )

@dp.message(F.text.lower().in_(['да','давай','сыграем','игра']))
async def process_positive_answer(message:types.Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number']= get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: types.Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
        )

@dp.message(lambda x:x.text and x.text.isdigit() and 1<= int(x.text) <=100)
async def process_numbers_answer(message: types.Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game']=False
            users[message.from_user.id]['total_games']+=1
            users[message.from_user.id]['wins']+=1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts']-=1
            await message.answer(
                'Мое число меньше'
            )
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts']-=1
            await message.answer(
                'Моё число больше'
            )
        if users[message.from_user.id]['attempts']==0:
            users[message.from_user.id]['in_game']=False
            users[message.from_user.id]['total_games']+=1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_message(message:types.Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )