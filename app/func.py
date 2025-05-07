from aiogram.types import LabeledPrice, CallbackQuery
import json

payment_api = ''



async def send_invoice(callback: CallbackQuery):
    price = [LabeledPrice(label='Месячная подписка', amount=500 * 100)]
    provider_data = json.dumps({
    "receipt": {
        "items": [
        {
            "description": f"User ID: {callback.from_user.id}",
            "quantity": 1,
            "amount": {
              "value": 500,
              "currency": "RUB"
            },
            "vat_code": 1,
            "payment_mode": "full_payment",
            "payment_subject": "service"
        }
        ]
    }
    })


    await callback.message.answer_invoice(
        title = 'Подписка на канал',
        description='Месячная подписка на закрытый тгк',
        provider_token=payment_api,
        currency='RUB', 
        need_email=True,
        send_email_to_provider=True,
        is_flexible=False,
        prices= price,
        start_parameter='channel_sub',
        payload=f'{callback.from_user.id}',
        provider_data=provider_data
    )

