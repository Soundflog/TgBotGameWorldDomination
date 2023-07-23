import requests as r
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from buttons.inlinebuttons.FormMainButton import in_Form_Main_Keyboard
from config.configurations import REQUEST_URL_WORLD, REQUEST_URL_FORM
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
        answerFromPassword = r.post(f"{REQUEST_URL_WORLD}/countrypassword", json=dataForPost)
        if answerFromPassword.ok:
            getFormCountry = r.get(f"{REQUEST_URL_FORM}/getFormCountry?countryId={country_id}").json()
            country_Info = getFormCountry['form']
            # ecology_info = country_Info['ecology']
            city_Info = {}
            if country_Info['countryId'] == country_id:
                city_Info = country_Info['friendlyCities']
            textForEdited = f"🌍 Мир 🌍\n" \
                            f"{world['title']}\n" \
                            f"🌱 Экология: <b>{round(world['ecology'], 2)} %</b>\n\n" \
                            f"🗺️ Страна 🗺️\n" \
                            f"<b>{country_Info['title']}</b>\n\n" \
                            f"💸 Баланс: <b>{country_Info['balanceInfo']} 💲</b>\n" \
                            f"🚀 Ракет: <b>{country_Info['rocketInfo']}</b> + {country_Info['rocket']}\n\n" \
                            f"🏙️ Города 🏙️\n"
            for city in city_Info:
                textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                                 f"🌿 Ур. жизни: {city['lifestandard']} %\n" \
                                 f"🛡️ Щит: {'✔️ ' if city['shieldInfo'] else '❌'} ---> {'✔️' if city['shield'] else '❌'}\n\n"
            await message.delete()
            await message.answer(
                text=textForEdited,
                parse_mode=ParseMode.HTML,
                reply_markup=in_Form_Main_Keyboard()
            )
            await state.clear()
            await state.set_state(CountryStates.main_keyboard)
            await state.update_data(form=getFormCountry, world=world)
            return
        await message.answer(text=f"Код ошибки:\n{answerFromPassword.status_code}")

    await state.clear()
    await message.answer("Некорректный тип сообщения")
