import datetime

from aiogram import Router, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

import config.configurations
from buttons.inlinebuttons.FormMainButton import in_Form_MoneyTransfer
from states.WorldStates import CountryStates
from datetime import datetime, timedelta

router = Router()


# ============================ ПОЗВАТЬ ВЕДУЩЕГО ==========================

@router.callback_query(lambda c: c.data == 'main_call', CountryStates.main_keyboard)
async def call_menu_callback(call: CallbackQuery, bot: Bot, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    textForEdited = f"<b>Вас вызывает</b>\n" \
                    f"🗺️ Страна 🗺️\n" \
                    f"<b>{country_Info['title']}</b>\n"
    lastTimeCall = user_data['throttling']
    time_delta = timedelta(seconds=15)
    if lastTimeCall + time_delta <= datetime.utcnow():
        await bot.send_message(
            chat_id=config.configurations.admins['id'],
            text=textForEdited,
            parse_mode=ParseMode.HTML,
        )
        await call.answer(
            text="Вы позвали ведущего, ожидайте",
            show_alert=True
        )
        await state.update_data(throttling=datetime.utcnow())
    else:
        await call.answer(
            text="Вы уже позвали ведущего"
        )
