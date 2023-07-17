from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import requests as r
import json

from buttons.inlinebuttons.chooseWorld import in_World_menu
from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD
from states.WorldStates import WorldStates, CountryStates

router = Router()


@router.callback_query(lambda c: c.data.startswith('country_'), WorldStates.after_choose_world)
async def update_keyboard_country(call: CallbackQuery, state: WorldStates.after_choose_world):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    world = user_data['world']
    split_callback_data = call.data.split('_')
    country_id = int(split_callback_data[1])
    await state.clear()
    await state.set_state(CountryStates.password)
    await state.update_data(country_id=country_id, world=world)
    await call.message.edit_text(
        text=f"Введите пароль для страны",
        inline_message_id=call.inline_message_id
    )


@router.message(CountryStates.password)
async def message_handler_country(message: Message, state: CountryStates.password):
    if message.text:
        user_data = await state.get_data()
        world = user_data['world']
        country_id = user_data['country_id']

        dataForPost = {"id": 0, "countryid": country_id, "password": str(message.text)}
        d = json.dumps(dataForPost)
        answerFromPassword = r.post(f"{REQUEST_URL_WORLD}/countrypassword", data=dataForPost)
        if answerFromPassword.ok:
            array_country_Info = world['countryInfos']
            country_Info = {}
            city_Info = {}
            for country in array_country_Info:
                print(f"country id: {country['id']}")
                if country['id'] == country_id:
                    print("Successful")
                    country_Info = country
                    city_Info = country['cityInfos']
                    break
            if country_Info is None or city_Info is None:
                await message.answer(
                    text="Произошла ошибка\n"
                         "Такой страны не существует или у страны нет городов"
                )

            await message.edit_text(
                text=f"🌍 Мир 🌍\n"
                     f"{world['title']}\n\n"
                     f"🗺️ Страна 🗺️\n"
                     f"{country_Info['title']}\n\n"
                     f"⚖️ Баланс: {country_Info['balance']}\n"
                     f"🌿 Уровень жизни: {country_Info['lifestandard']} %\n"
                     f"🚀 Ракет: {country_Info['rocket']}\n\n"
                     f"🏙️ Города 🏙️\n"
                     f"1: {city_Info[0]['title']}\n"
                     f"2: {city_Info[1]['title']}\n"
                     f"3: {city_Info[2]['title']}\n"
                     f"4: {city_Info[3]['title']}",
                chat_id=message.chat.id
            )
            return
        await message.answer(text=f"Код ошибки:\n{answerFromPassword.status_code}")

    await state.clear()
    await message.answer("Некорректный тип сообщения")
