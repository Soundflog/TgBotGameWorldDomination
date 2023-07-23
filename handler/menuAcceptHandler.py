from datetime import datetime, timedelta

import requests as r
from aiogram import Router
from aiogram.types import CallbackQuery

from config.configurations import REQUEST_URL_FORM
from methods import ReCalcBalance
from states.WorldStates import CountryStates

router = Router()


# ============================ ACCESS ==========================

@router.callback_query(lambda c: c.data == 'main_access', CountryStates.main_keyboard)
async def accept_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    world = user_data['world']
    # dataForPost = {"id": 0, "countryid": country_id, "password": str(message.text)}
    # answerFromPassword = r.post(f"{REQUEST_URL_WORLD}/countrypassword", json=dataForPost)
    if country_Info['balanceInfo'] >= 0:
        answerFromSetForm = r.post(f"{REQUEST_URL_FORM}/setFormCountry", json=country_Info)
        if answerFromSetForm.ok:
            await call.answer(
                text="Отправлено, ожидайте окончания раунда"
            )
            getFormCountry = r.get(f"{REQUEST_URL_FORM}/getFormCountry?countryId={country_Info['countryId']}").json()
            # getFormCountry['form']['balanceInfo'] = country_Info['balanceInfo']
            await state.clear()
            await state.set_state(CountryStates.main_keyboard)
            await state.update_data(
                form=getFormCountry,
                world=world,
                throttling=datetime.utcnow() - timedelta(seconds=15)
            )
        else:
            await call.answer(
                text="Что-то пошло не так ... =("
            )
    else:
        await call.answer(
            text="Отрицательный баланс!",
            show_alert=True
        )
