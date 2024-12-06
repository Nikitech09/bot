import asyncio
import sys
import logging
from bot_logic.bot import cmd_start
from bot_logic.loader import dp, bot
from config.config import load_config

config = load_config('.env')

async def main() -> None:
    dp.message.register(cmd_start)
    #dp.message.register(echo_handler)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())