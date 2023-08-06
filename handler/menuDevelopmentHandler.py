from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Development_TrueFalse, in_Form_Main_Keyboard
from methods import ReCalcBalance
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
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"🏙️<b>Развитие городов</b>🏙️\n" \
                    f"<b>150 💲</b>\n\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🌿 Развитие: {str(city['lifestandard']) + ' + 20 ' if city['development'] else city['lifestandard']} %\n\n"
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
    selected_cities = user_data.get('selectedDev')
    if selected_cities is not None:
        selected_cities = user_data['selectedDev']
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
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"🏙️<b>Развитие городов</b>🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🌿 Развитие: {str(city['lifestandard']) + ' + 20 ' if city['development'] else city['lifestandard']} %\n\n"

    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Development_TrueFalse(city_Info)
    )
    await state.update_data(selectedDev=selected_cities)


# ======================================= BACK TO MENU =======================
@router.callback_query(lambda c: c.data == "dev_menu", CountryStates.main_keyboard)
async def callback_dev_back_to_menu(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    world = user_data['world']
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🌍 Мир 🌍\n" \
                    f"{world['title']}\n" \
                    f"🌱 Экология: <b>{round(world['ecology'], 2)} %</b>\n\n" \
                    f"🗺️ Страна 🗺️\n" \
                    f"<b>{country_Info['title']}</b>\n\n" \
                    f"💸 Баланс: <b>{country_Info['balanceInfo']} 💲</b>\n" \
                    f"🚀 Ракет: <b>{country_Info['rocket']}</b> | {country_Info['rocketInfo']}\n\n" \
                    f"🏙️ Города 🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🌿 Развитие: {str(city['lifestandard']) + ' + 20 ' if city['development'] else city['lifestandard']} %\n\n"
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Main_Keyboard()
    )
