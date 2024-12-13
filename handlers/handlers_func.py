import requests
import tiktoken
from aiogram import Router
from aiogram.types import Message

router = Router()
bot = None

def set_bot(instance):
    global bot
    bot = instance

async def new_user(message: Message):
    nu_username = message.from_user.full_name
    nu_id = message.from_user.id
    await bot.send_message(684304640, f'Новый пользователь! {nu_username}, id:{nu_id}')

async def get_full_balance(url, token):
    url = url
    headers = {
    "Authorization": token  
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        resultjsn = response.json()
        result = resultjsn['balance'] 
        return str(result)
    else:
        return (
            f"Error: {response.status_code}, {response.text}"
        )

def text_price(prompt, completion, cost_for_question = 0.1728, cost_for_answer = 0.0432):
    total_price = (prompt/1000) * cost_for_question + (completion/1000) * cost_for_answer
    return total_price

