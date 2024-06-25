from aiogram import types

async def get_inline_main():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text= "подать заявку", callback_data='invate'),
        types.InlineKeyboardButton(text= "статус", callback_data='status'),
    ]
    markup.add(*buttons)
    return markup

async def get_inline1():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text= "заявка", callback_data='invate'),
        types.InlineKeyboardButton(text= "статус", callback_data='status'),
    ]
    markup.add(*buttons)
    return markup


async def get_invate():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text= "назад", callback_data='button1')
    ]
    markup.add(*buttons)
    return markup

async def get_status():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text= "назад", callback_data='button1')
    ]
    markup.add(*buttons)
    return markup
