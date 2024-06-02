import asyncio
import sys
import logging
from bot_logic.bot import cmd_start, echo_handler
from bot_logic.loader import dp, bot

async def main() -> None:
    dp.message.register(cmd_start)
    dp.messgae.register(echo_handler)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())