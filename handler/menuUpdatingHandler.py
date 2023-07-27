from datetime import datetime, timedelta

import requests as r
from aiogram import Router
from aiogram.types import CallbackQuery

from config.configurations import REQUEST_URL_FORM
from methods import ReCalcBalance
from states.WorldStates import CountryStates

router = Router()


# ============================ Update ==========================

@router.callback_query(lambda c: c.data == 'main_update', CountryStates.main_keyboard)
async def update_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    world = user_data['world']
    getFormCountry = r.get(f"{REQUEST_URL_FORM}/getFormCountry?countryId={country_Info['countryId']}").json()
    await state.clear()
    await state.set_state(CountryStates.main_keyboard)
    await state.update_data(
        form=getFormCountry,
        world=world,
        throttling=datetime.utcnow() - timedelta(seconds=15)
    )
    await call.answer(
        text="Обновлено"
    )
