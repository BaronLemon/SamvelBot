import logging
import os
from aiogram import Bot, Dispatcher, F
from app.handlers.base import rt
from config import TOKEN
from app.schedule import check_subscriptions
from dotenv import load_dotenv
import asyncio

load_dotenv()

bot_api = os.getenv('TOKEN')

async def main():
    async with Bot(token=bot_api) as bot:
        dp = Dispatcher()
        dp.include_router(rt)

        try:
            asyncio.create_task(check_subscriptions(bot))
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)

        finally:
            print('Bot is closed')

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    try: 
        asyncio.run(main())

    except KeyboardInterrupt:
        print('Exit')

