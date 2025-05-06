from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.filters import CommandStart
from aiogram import F, Router, Bot
import app.keyboards as kb
from app.func import send_invoice
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from db.subs import add_or_update_subscription



invite_link = 'https://t.me/+sDgRD76MeIYzODdi'
CHANNEL_ID = '-1002009310043'
rt = Router()


@rt.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
f"""👋 Привет, {message.from_user.first_name}!

Добро пожаловать в наш финансовый мир!""",
reply_markup=kb.info_btn)


@rt.callback_query(F.data == 'info')
async def about_channel(callback: CallbackQuery):
    await callback.message.answer(
"""Наш канал — это путеводитель в мире личных финансов и инвестиций 

Здесь вы найдете полезные советы по управлению бюджетом, стратегии накопления и приумножения капитала

Мы поможем вам развить финансовую грамотность и научим, как сделать так, чтобы деньги работали на вас

Присоединяйтесь к нам и откройте для себя искусство финансового мира!""",
reply_markup=kb.pay_btn)



@rt.callback_query(F.data == 'pay')
async def invoice(callback: CallbackQuery):
    await send_invoice(callback)
    

@rt.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok = True)


@rt.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):


    msk_time = ZoneInfo("Europe/Moscow")
    await add_or_update_subscription(user_id=message.from_user.id, expires_at=datetime.now(msk_time) + timedelta(days=30))

    try:
        user_first_name = message.from_user.first_name
        invite = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1,
            expire_date=datetime.now(msk_time) + timedelta(days=1),
            name=f'Подписка для {user_first_name}'
        )

        await message.answer(
            f"✅ Спасибо за оплату подписки!\n\n"
            f"Вот твоя личная ссылка на вступление в закрытый канал:\n"
            f"{invite.invite_link}\n\n"
            f"⚠️ Ссылка действительна 24 часа и только для тебя.", disable_web_page_preview=True
        )



    except Exception as e:
        await message.answer("❌ Ошибка при создании ссылки. Попробуйте позже.\n\n Тех. поддержка: @samokha_menegr")

    