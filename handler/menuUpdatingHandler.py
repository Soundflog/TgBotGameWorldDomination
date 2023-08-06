from contextlib import suppress
from datetime import datetime, timedelta

import requests as r
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Main_Keyboard
from config.configurations import REQUEST_URL_FORM, REQUEST_URL_WORLD
from methods import ReCalcBalance
from methods.ReCalcBalance import RocketCalc, BalanceInNewRound, BalanceCalc
from states.WorldStates import CountryStates

router = Router()


# ============================ Update ==========================

@router.callback_query(lambda c: c.data == 'main_update', CountryStates.main_keyboard)
async def update_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    world = user_data['world']
    UpdateGetFormCountry = r.get(f"{REQUEST_URL_FORM}/getFormCountry?countryId={country_Info['countryId']}").json()
    UpdateWorld = r.get(f"{REQUEST_URL_WORLD}/world?worldId={world['id']}").json()['worldInfo']
    await state.clear()
    await state.set_state(CountryStates.main_keyboard)
    await state.update_data(
        form=UpdateGetFormCountry,
        world=UpdateWorld,
        throttling=datetime.utcnow() - timedelta(seconds=15)
    )
    await call.answer(
        text="Обновлено"
    )
    user_data = await state.get_data()
    world = user_data['world']
    ecology = world['ecology']
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    rockets = RocketCalc(country_Info)
    incomeBalance = BalanceInNewRound(country_Info, ecology)
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🌍 Мир 🌍\n" \
                    f"{world['title']}\n\n" \
                    f"🌱 Экология: <b>{round(ecology, 2)} %</b>\n\n" \
                    f"🗺️ Страна 🗺️\n" \
                    f"<b>{country_Info['title']}</b>\n\n" \
                    f"💸 Баланс: <b>{country_Info['balanceInfo']}</b> $ (+<b>{round(incomeBalance)}</b> $)\n" \
                    f"🚀 Ракет: <b>{rockets}</b> | {country_Info['rocket']}\n\n" \
                    f"🏙️ Города 🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🌿 Ур. жизни: {city['lifestandard']} %\n" \
                         f"🛡️ Щит: {'✔️ ' if city['shieldInfo'] else '❌'} ---> {'✔️' if city['shield'] else '❌'}\n\n"
    textForEdited += "<i>Ведущий сообщит Вам об окончании раунда</i>"
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            text=textForEdited,
            inline_message_id=call.inline_message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=in_Form_Main_Keyboard()
        )
