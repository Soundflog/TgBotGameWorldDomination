from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Development_TrueFalse, in_Form_Main_Keyboard
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс РАЗВИТИЕ ГОРОДОВ ==========================
@router.callback_query(lambda c: c.data == 'main_development', CountryStates.main_keyboard)
async def menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"⚖️{country_Info['balanceInfo']}⚖️\n\n" \
                    f"🏙️<b>Развитие городов</b>🏙️\n" \
                    f"<b>150$</b>\n\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title']}</b>\n" \
                         f"🌿 Ур. жизни: {str(city['lifestandard']) + ' + 20 %' if city['development'] else city['lifestandard']}\n" \
                         f"Состояние: {'✅' if city['condition'] else '🔴'}\n" \
                         f"Щит: {'✅' if city['shield'] else '🔴'}\n\n"
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Development_TrueFalse(city_Info)
    )


# ===================================== РАЗВИТИЕ ГОРОДОВ ======================
@router.callback_query(lambda c: c.data.startswith("city_development_"), CountryStates.main_keyboard)
async def callback_city_development(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    split_callback_data = call.data.split('_')
    city_id = int(split_callback_data[2])
    selected_cities = user_data.get('selected')
    if selected_cities is not None:
        selected_cities = user_data['selected']
    else:
        selected_cities = []
    for city in city_Info:
        if city["cityId"] == city_id and city['development'] is False:
            country_Info['balanceInfo'] -= 150
            city['development'] = True
            selected_cities.append(city)
            await call.answer(
                text=f"Повышен уровень жизни в городе {city['title']}"
            )
            continue
        if city["cityId"] == city_id and city['development'] is True:
            country_Info['balanceInfo'] += 150
            city['development'] = False
            selected_cities.remove(city)
            await call.answer(
                text=f"Отмена повышения ур. жизни в городе {city['title']}"
            )
            continue

    textForEdited = f"🗺️ Страна 🗺️\n{country_Info['title']}\n" \
                    f"⚖️{country_Info['balanceInfo']}⚖️\n\n" \
                    f"🏙️<b>Развитие городов</b>🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title']}</b>\n" \
                         f"🌿 Ур. жизни: {str(city['lifestandard']) + ' + 20 %' if city['development'] else city['lifestandard']}\n" \
                         f"Состояние: {'✅' if city['condition'] else '🔴'}\n" \
                         f"Щит: {'✅' if city['shield'] else '🔴'}\n\n"

    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Development_TrueFalse(city_Info)
    )
    await state.update_data(selected=selected_cities)
    # await call.message.edit_text(
    #     text=f"🗺️ Страна 🗺️\n"
    #          f"{country_Info['title']}\n\n"
    #          f"<b>Развитие городов</b>\n"
    #          f"<b>{city_Info[0]['title']}</b>\n"
    #          f"🌿 Ур. жизни: {str(city_Info[0]['lifestandard']) + ' + 20 %' if city_Info[0]['development'] else city_Info[0]['lifestandard']}\n"
    #          f"Состояние: {'✅' if city_Info[0]['condition'] else '🔴'}\n"
    #          f"Щит: {'✅' if city_Info[0]['shield'] else '🔴'}\n\n"
    #          f"<b>{city_Info[1]['title']}</b>\n"
    #          f"🌿 Ур. жизни: {str(city_Info[1]['lifestandard']) + ' + 20 %' if city_Info[1]['development'] else city_Info[1]['lifestandard']}\n"
    #          f"Состояние: {'✅' if city_Info[1]['condition'] else '🔴'}\n"
    #          f"Щит: {'✅' if city_Info[1]['shield'] else '🔴'}\n\n"
    #          f"<b>{city_Info[2]['title']}</b>\n"
    #          f"🌿 Ур. жизни: {str(city_Info[2]['lifestandard']) + ' + 20 %' if city_Info[2]['development'] else city_Info[2]['lifestandard']}\n"
    #          f"Состояние: {'✅' if city_Info[2]['condition'] else '🔴'}\n"
    #          f"Щит: {'✅' if city_Info[2]['shield'] else '🔴'}\n\n"
    #          f"<b>{city_Info[3]['title']}</b>\n"
    #          f"🌿 Ур. жизни: {str(city_Info[3]['lifestandard']) + ' + 20 %' if city_Info[3]['development'] else city_Info[3]['lifestandard']}\n"
    #          f"Состояние: {'✅' if city_Info[3]['condition'] else '🔴'}\n"
    #          f"Щит: {'✅' if city_Info[3]['shield'] else '🔴'}",
    #     parse_mode=ParseMode.HTML,
    #     reply_markup=in_Form_Development_TrueFalse(city_Info)
    # )


@router.callback_query(lambda c: c.data == "dev_menu", CountryStates.main_keyboard)
async def callback_back_to_menu(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    world = user_data['world']
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    textForEdited = f"🌍 Мир 🌍\n" \
                    f"{world['title']}\n" \
                    f"🌱 Экология: <b>{round(world['ecology'], 2)} %</b>\n\n" \
                    f"🗺️ Страна 🗺️\n" \
                    f"<b>{country_Info['title']}</b>\n\n" \
                    f"⚖️ Баланс: <b>{country_Info['balanceInfo']}</b>\n" \
                    f"🚀 Ракет: <b>{country_Info['rocket']}</b> | {country_Info['rocketInfo']}\n\n" \
                    f"🏙️ Города 🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title']}</b>\n" \
                         f"🌿 Ур. жизни: {str(city['lifestandard']) + ' + 20 %' if city['development'] else city['lifestandard']}\n" \
                         f"Состояние: {'✅' if city['condition'] else '🔴'}\n" \
                         f"Щит: {'✅' if city['shield'] else '🔴'}\n\n"
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Main_Keyboard()
    )
