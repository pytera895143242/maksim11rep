from aiogram import types
from misc import dp,bot
import asyncio
from .sqlit import get_info_key,get_info_fav
from .find_mov import find_m
from .generate_markup import subscription_markup, check_subscription
from config import films,url_admin

@dp.message_handler(content_types='text')
async def all_other_messages(message: types.message):
    if await check_subscription(message.chat.id) == True:
        if message.text == "Поиск фильмов 🔎":
            photo = open("img/main.jpg", 'rb')
            await bot.send_photo(message.chat.id, photo=photo, caption="""<b>Вы запустили поиск фильмов 🔎</b> \n\nНапишите мне название фильма или сериала...""")

        elif message.text == "Фильм из ТикТок 🎬":
            await message.answer("<b>Введите номер фильма</b>")

        elif message.text == "Случайный выбор 🎊":
            for f in films:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🖥 Смотреть фильм', url=f[1])
                bat_b = types.InlineKeyboardButton(text='⭐️ Добавить в избранное', callback_data=f'iz_{f[1][46:]}')
                markup.add(bat_a)
                markup.add(bat_b)
                with open(f[0], 'rb') as photo:
                    await bot.send_photo(message.chat.id, photo=photo,caption=f[2],reply_markup=markup)

        elif message.text == "Избранное ❤️":
            fav_txt = ""
            data_f = get_info_fav(message.chat.id)
            for f in data_f:
                fav_txt += f"<a href = '{f[1]}'>" + f"👉🏻 {f[2]}..." + "</a>" + "\n"

            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='🗑 Удалить все', callback_data='del_fav')
            markup.add(bat_a)
            photo = open("img/main.jpg", 'rb')
            await bot.send_photo(message.chat.id, photo=photo, caption=f"""<b>Пришло время посмотреть что-то из избранного? \n\n{fav_txt}\nФильмы в избранном </b>""",reply_markup=markup)

        #
        # elif message.text == "Информация ⚙️":
        #     markup = types.InlineKeyboardMarkup()
        #     bat_a = types.InlineKeyboardButton(text='👨🏻‍💻 Администратор', url=url_admin)
        #     markup.add(bat_a)
        #     photo = open("img/main.jpg", 'rb')
        #     await bot.send_photo(message.chat.id, photo=photo,caption="""<b>Краткий информационный стенд кинотеатра 🎥</b>\n\n0\n\nПо всем вопросам обращайтесь к администратору""",reply_markup=markup)

        elif message.text == "FAQ ?":
            await message.answer("Если Вы владелец авторских прав или его представитель, просим Вас учесть, что все ссылки в боте берутся из сторонних источников, сайтов, видео-хостингов. Мы не имеем отношения к размещенным материалам по этим ссылкам. \n\nБот работает по принципу поисковой системы.")
        else:
            info = (get_info_key(message.text))
            if len(info) != 0:
                await message.answer(f"{message.text} - {info[0][2]}")

            else:
                await find_m(message)
    else:
        photo = open("img/main.jpg", 'rb')
        await bot.send_photo(message.chat.id, photo=photo,caption="""<b>⭐️ Для полноценного использования КИНОБОТА, подпишитесь на наших спонсоров:</b>""",reply_markup=subscription_markup())


@dp.message_handler(content_types='photo')
async def all_fdsfdsessages(message: types.message):
    pass