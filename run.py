import logging
from aiogram import Bot, Dispatcher, F
from app.handlers.base import rt
from config import TOKEN
from app.schedule import check_subscriptions
import asyncio


bot_api = TOKEN


bot = Bot(token=bot_api)
dp = Dispatcher()
dp.include_router(rt)



async def main():
    asyncio.create_task(check_subscriptions(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    try: 
        asyncio.run(main())

    except KeyboardInterrupt:
        print('Exit')

