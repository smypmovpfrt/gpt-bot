from openai import AsyncOpenAI
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_actions import Bot_db
from config_reader import user_contexts, user_settings, config
from handlers.handlers_func import text_price
from text_replies.all import balance_over

BASE_URL = config.base_url
API_KEY = config.api_key
BALANCE_URL = 'https://api.proxyapi.ru/proxyapi/balance'
cost_for_question = 0.2 # 0.1728 
cost_for_answer = 0.0632 # 0.0432
MAX_MESSAGE_LENGTH = 4000
router = Router()
bot = None
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
    )

def set_bot(instance):
    global bot
    bot = instance

@router.message(F.text)
async def handle_message(my_message: types.Message):
    user_id = my_message.from_user.id
    inline_keyboard_components = []
    clear_context_btn = [InlineKeyboardButton(text='Новый диалог', callback_data='clear_context')]
    inline_keyboard_components.append(clear_context_btn)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard_components)
    db_for_bal = Bot_db()
    if db_for_bal.is_active(user_id) == 1: 
        old_balance = db_for_bal.get_user_balance(user_id=user_id)
        db_for_bal.close()
        get_user_settings = user_settings.get(my_message.chat.id)
        try:
            context_length = get_user_settings.get('context_length')
        except:
            context_length = 3    
        if user_id not in user_contexts:
            user_contexts[user_id] = []
        user_input = my_message.text
        user_contexts[user_id].append({"role": "user", "content": user_input})
        while len(user_contexts[user_id]) > context_length * 2:
            user_contexts[user_id].pop(0)
        notification_message = await my_message.answer("⏳")
        response = await client.chat.completions.create(
            messages=user_contexts[user_id], 
            model= "gpt-4o-mini"
        )
        answer = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_request_price = text_price(prompt_tokens, completion_tokens, cost_for_question, cost_for_answer)
        new_balance = old_balance - total_request_price
        user_contexts[user_id].append({"role": "assistant", "content": answer})
        db = Bot_db()
        if new_balance < 0:
            db.update_user_balance(user_id, new_balance=new_balance)
            db.not_active(user_id=user_id)
            db.close()
        else:
            db.update_user_balance(user_id, new_balance=new_balance)
            db.close()
        if len(answer) > MAX_MESSAGE_LENGTH:
            parts = [answer[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(answer), MAX_MESSAGE_LENGTH)]
            for part in parts:
                try:
                    await my_message.reply(part,reply_markup=inline_keyboard, parse_mode='Markdown')
                except:
                    await my_message.reply(part,reply_markup=inline_keyboard)    
        else:
                try:
                    await my_message.reply(answer,reply_markup=inline_keyboard, parse_mode='Markdown')
                except:
                    await my_message.reply(part,reply_markup=inline_keyboard) 

        await notification_message.delete()
    else:
        await my_message.answer(balance_over(), parse_mode='MarkdownV2')
