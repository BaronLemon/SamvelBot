from aiogram.types import LabeledPrice, CallbackQuery

payment_api = 'payment_API'


async def send_invoice(callback: CallbackQuery):
    price = [LabeledPrice(label='Месячная подписка', amount=50000)]
    await callback.message.answer_invoice(
        title = 'Подписка на канал',
        description='Месячная подписка на закрытый тгк',
        prices = price, 
        need_email=True,
        send_email_to_provider=True,
        provider_token=payment_api,
        payload='channel_sub',
        currency='RUB'
    )

