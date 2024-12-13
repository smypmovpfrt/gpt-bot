from aiogram import Router, types, F
from config_reader import user_contexts
router = Router()

@router.callback_query(F.data == "clear_context")
async def clear_context(callback: types.CallbackQuery):
    context_for_clearing = user_contexts.get(callback.message.from_user.id, {})
    context_for_clearing.clear()
    await callback.message.answer("*Контекст отчищен!*", parse_mode='Markdown')
    await callback.answer()    