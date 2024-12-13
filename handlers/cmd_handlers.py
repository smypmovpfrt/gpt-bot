from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import db_actions
from config_reader import user_contexts, user_settings
from text_replies.all import start_reply
from handlers.handlers_func import get_full_balance, new_user
from handlers.txt_handlers import BALANCE_URL, API_KEY
from text_replies.all import set_context_msg, about_context_msg

router = Router()
bot = None

def set_bot(instance):
    global bot
    bot = instance



@router.message(Command("start")) 
async def cmd_start(message: Message):
    user_settings[message.chat.id] = {
        'context_length' : 3
    }
    db = db_actions.Bot_db()
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.close()
        await new_user(message=message)
    await message.answer(start_reply())

@router.message(Command("users_count"))
async def show_users_count(message: Message):
    if message.from_user.id == 684304640:
        db = db_actions.Bot_db()
        message.reply(db.get_users_count()) 
        db.close()

@router.message(Command("api_balance"))
async def get_api_balance(message: Message):
    if message.from_user.id==684304640:
        balance = await get_full_balance(BALANCE_URL, API_KEY)
        await message.answer(balance)
    else: 
        await message.answer('only for administrator')    

@router.message(Command("balance"))
async def get_api_balance(message: Message):
    db = db_actions.Bot_db()
    user_balance = db.get_user_balance(message.from_user.id)
    await message.answer(f'{user_balance:.3f} rub.')

@router.message(Command("context")) 
async def def_context(message: Message, command):
    if command.args is None:
        await message.answer(set_context_msg(), parse_mode='Markdown')
    new_context_length = command.args.split(" ", maxsplit = 1)
    user_settings[message.chat.id] = {
        'context_length' : int(new_context_length[0])
    }
    await message.answer(
        f"*Новая длинна диалога:*\n"
        f"{new_context_length} сообщений"
    ,parse_mode='Markdown') 

@router.message(Command("settings"))
async def show_settings(message: Message):
    get_context_length = user_settings[message.from_user.id]
    context_length = get_context_length['context_length']
    await message.answer(f'*Текущая длина диалога:*\n'
                         f'{context_length} сообщений', parse_mode='Markdown')

@router.message(Command("clear_context")) 
async def def_context(message: Message):
    context_for_clearing = user_contexts.get(message.from_user.id, {})
    context_for_clearing.clear()
    await message.answer("Контекст отчищен!", parse_mode='Markdown')


@router.message(Command("help")) 
async def show_help(message: Message):
    await message.answer(about_context_msg() ,parse_mode='Markdown'
    )

@router.message(Command("add_balance"))
async def show_users_count(message: Message):
    if message.from_user.id == 684304640 or message.from_user.id == 7855182897:
        db = db_actions.Bot_db()
        db.update_user_balance(message.from_user.id, 100)
        db.close()
        await message.reply("Бабло зачислено!")
    else:
        await message.reply("Вы не админ!")    


@router.message(Command("makemeac"))
async def show_users_count(message: Message):
    if message.from_user.id == 684304640 or message.from_user.id == 7855182897:
        db = db_actions.Bot_db()
        db.not_active(message.from_user.id, 1)
        db.close()
        await message.reply("Бабло зачислено!")
    else:
        await message.reply("Вы не админ!")    
