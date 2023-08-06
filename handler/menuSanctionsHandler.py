from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Sanctions
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс САНКЦИИ ==========================
@router.callback_query(lambda c: c.data == 'main_sanctions', CountryStates.main_keyboard)
async def sanctions_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n\n" \
                    f"👎<b>САНКЦИИ</b>👎\n\n"
    for enemyCountry in country_Info['enemyCountries']:
        textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                         f"Санкция: {'➖' if enemyCountry['sanctions'] else '👎'}\n\n"
    selected_country_sanctions = user_data.get('sanctions')
    if selected_country_sanctions is not None:
        selected_country_sanctions = user_data['sanctions']
    else:
        selected_country_sanctions = []
    for enemyCountry in country_Info['enemyCountries']:
        if enemyCountry['sanctions'] is True:
            selected_country_sanctions.append(enemyCountry['countryId'])
    textForEdited += "<i>👎 - Санкция наложена</i>\n" \
                     "<i>➖ - Санкции нет</i>\n"
    await state.update_data(sanctions=selected_country_sanctions)
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Sanctions(country_Info['enemyCountries'])
    )


# country_sanctions_
@router.callback_query(lambda c: c.data.startswith('country_sanctions_'), CountryStates.main_keyboard)
async def choose_enemy_country_sanctions_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    split_callback_data = call.data.split('_')
    country_id_for_sanction = int(split_callback_data[2])
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"👎<b>САНКЦИИ</b>👎\n\n" \
                    f"На страны:\n"
    selected_country_sanctions = user_data.get('sanctions')
    if selected_country_sanctions is not None:
        selected_country_sanctions = user_data['sanctions']
    else:
        selected_country_sanctions = []
    for enemyCountry in country_Info['enemyCountries']:
        if enemyCountry['countryId'] == country_id_for_sanction:
            if enemyCountry['sanctions'] is False:
                selected_country_sanctions.append(enemyCountry['countryId'])
                enemyCountry['sanctions'] = True

            else:
                selected_country_sanctions.remove(enemyCountry['countryId'])
                enemyCountry['sanctions'] = False
        textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                         f"Санкция: {'➖' if enemyCountry['sanctions'] else '👎'}\n\n"
    textForEdited += "<i>👎 - Санкция наложена</i>\n" \
                     "<i>➖ - Санкции нет</i>\n"
    await state.update_data(sanctions=selected_country_sanctions)
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Sanctions(country_Info['enemyCountries'])
    )