import logging
import json
import data 
import InlineButton
import time
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from datetime import datetime

API_TOKEN = data.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

JSON_FILE = data.FILE

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = await InlineButton.get_inline_main()
    await message.reply(f"Привет, {message.from_user.first_name}")
    await message.answer(
       "В этом боте ты можешь подать заявку на вступление в Винтрехолд",
       reply_markup=markup,
       disable_web_page_preview=True
    )

def chack_status(user_id) -> bool:
    with open("messages.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for b in data:
            if(b['status'] == True and b['user_id'] == user_id):
                return True
        return False

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    if(callback_query.data == "button1"):
        markup = await InlineButton.get_inline1()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text= "В этом боте ты можешь подать заявку на вступление в Винтерхолд",
                                reply_markup=markup,
                                parse_mode="HTML",
                                disable_web_page_preview=True)
        
    elif(callback_query.data == "invate"):
        markup = await InlineButton.get_invate()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text= f"Напиши свой возраст\n\nВаш дискорд\n\nРасскажи о своём опыте игры в майнкрафт, умеешь ли ты пользоваться лайтматикой(если нет, то мы обучим)\n\nЧем бы ты хотел заниматься(строительство, добыча ресурсов, переносить готовые постройки, строить фермы, заниматься творческой составляющей нашего города)",
                                reply_markup=markup,
                                parse_mode="HTML",
                                disable_web_page_preview=True)
        chack()

    elif(callback_query.data == "status"):
        markup = await InlineButton.get_status()
        if(chack_status(callback_query.from_user.id)):
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text= "Ваша заявка одобрена✅",
                                    reply_markup=markup,
                                    parse_mode="HTML",
                                    disable_web_page_preview=True)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text= "Ваша заявка на рассмотрении❌",
                                    reply_markup=markup,
                                    parse_mode="HTML",
                                    disable_web_page_preview=True)
            sticker_id = 'CAACAgIAAxkBAAEGaqVmeqUj0KryeGNnMH3U62iEi0BGJQACAyUAAutvYUkL1g53P5QZvjUE'  # Замените на ID вашего стикера
            await bot.send_sticker(callback_query.message.chat.id, sticker_id)
            
        
    elif(callback_query.data == "back"):
        markup = await InlineButton.get_inline_main()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text= "В этом боте вы можете найти нужную для вас информацию о городе,\nа также подать заявку на вступление",
                                reply_markup=markup,
                                parse_mode="HTML",
                                disable_web_page_preview=True)
        
def save_message(data):
    try:
        with open(JSON_FILE, 'r+', encoding='utf-8') as file:
            try:
                messages = json.load(file)
            except json.JSONDecodeError:
                messages = []
            messages.append(data)
            file.seek(0)
            json.dump(messages, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump([data], file, ensure_ascii=False, indent=4)

def chack():
    @dp.message_handler()
    async def log_message(message: types.Message):
        with open("messages.json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
            username =[entry.get('user_id') for entry in data]
            for data in username:
                if(data == message.from_user.id):
                    await message.reply("Вы уже подали заявку!!\nСкоро поступит ответ")
                    time.sleep(0.2)
                    markup = await InlineButton.get_inline_main()
                    await message.answer(
                    "В этом боте ты можешь подать заявку на вступление в Винтрехолд",
                    reply_markup=markup,
                    disable_web_page_preview=True)
                    return
        user_id = message.from_user.id
        user_message = message.text
        user_first_name = message.from_user.first_name
        username = message.from_user.username or 'не указано'
        timestamp = datetime.now().isoformat()

        data = {
            'user_id': user_id,
            'first_name': user_first_name,
            'username': username,
            'message': user_message,
            'status': False,
            'timestamp': timestamp
        }

        save_message(data)

        await message.reply("Ваша заявка сохранена.")


        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)