from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




pay_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Покупаю!', callback_data='pay', pay=True)]
    ]
)

info_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='О канале', callback_data='info')]
    ]
)