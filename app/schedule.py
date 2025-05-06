import asyncio
from datetime import datetime, timedelta
from db.subs import get_all_subscriptions, remove_user
from db.models import async_session
import app.keyboards as kb
from aiogram import Bot
import traceback
from zoneinfo import ZoneInfo

CHANNEL_ID = '-1002009310043'  # укажи username или ID канала (бот должен быть админом)
CHECK_INTERVAL = 3600 * 12     # проверка срока подписки каждые 24 часа

async def check_subscriptions(bot: Bot):
    while True:

        async with async_session() as session:
            users = await get_all_subscriptions()

            for sub in users:
                user_id = sub.user_id
                msk_time = ZoneInfo('Europe/Moscow')
                now = datetime.now(msk_time)
                expires = sub.expires_at.astimezone(msk_time)

                delta = expires - now

                try:
                    if delta <= timedelta(seconds=0):
                        try:
                            await bot.send_message(user_id, "❌ Срок подписки истёк. Вы были удалены из канала.")
                            await bot.ban_chat_member(CHANNEL_ID, user_id)
                            await bot.unban_chat_member(CHANNEL_ID, user_id)  # чтобы он мог вернуться после оплаты
                            await remove_user(user_id)
                        except Exception as e:
                            print(f"Ошибка при удалении {user_id}: {e}")

                    elif delta <= timedelta(days=1):
                        await bot.send_message(user_id, "⚠️ Ваша подписка заканчивается через 1 день! Продлите, чтобы остаться в канале.", reply_markup=kb.pay_btn)

                    elif delta <= timedelta(days=3):
                        await bot.send_message(user_id, "🔔 Осталось 3 дня до окончания подписки. Не забудьте продлить!", reply_markup=kb.pay_btn)
                except Exception as e:
                    print(f"[ОШИБКА] user_id={user_id}, ошибка при действии: {e}")
                    traceback.print_exc()


        await asyncio.sleep(CHECK_INTERVAL)
