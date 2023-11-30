from aiogram import types
from misc import dp, bot
from .sqlit import get_info_all_key,reg_tiktok,delite_all_key
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg_kkey(StatesGroup):
    traf1 = State()
    traf2 = State()
    traf3 = State()
    traf4 = State()


# НАСТРОЙКА КЛЮЧЕЙ
@dp.callback_query_handler(text='set_key')
async def setkey212(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='Добавить ключ', callback_data='add_key')
    bat_b = types.InlineKeyboardButton(text='Удалить все ключи', callback_data='delite_key')
    markup_traf.add(bat_a)
    markup_traf.add(bat_b)

    text = ""
    ans = get_info_all_key()
    for a in ans:
        text +=  a[0] + " -- " + f"<a href = '{a[3]}'>" + a[2][0:16] + "..." + "\n" + "</a>"

    await bot.send_message(call.message.chat.id, text=f'Список активных ключей:\n\n\n'
                                                      f'{text}',reply_markup=markup_traf,disable_web_page_preview=True)

@dp.callback_query_handler(text='delite_key')
async def addkey212(call: types.callback_query):
    try:
        delite_all_key()
        await call.message.answer("Все ключи успешно удалены")
    except:
        await call.message.answer("Произошла ошибка при удалении ключей")



@dp.callback_query_handler(text='add_key')
async def addkey212(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text=f'Регистрация в формате: Номер - Название фильма')
    await reg_kkey.traf1.set()

@dp.message_handler(state=reg_kkey.traf1, content_types='text')
async def key_obnovlenie1(message: types.Message, state: FSMContext):
    x = (message.text).split("\n")
    for y in x:
        t = y.split(" - ")
        if len(t) == 2:
            try:
                reg_tiktok(t[0],t[1])
                await message.answer("Ключ успешно зарегистрирован!")
            except:
                await message.answer("Произошла ошибка...")
        else:
            await message.answer('Неверный формат')

    await state.finish()
