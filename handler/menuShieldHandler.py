from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Main_Keyboard, \
    in_Form_Shield_TrueFalse
from methods.ReCalcBalance import RocketCalc, BalanceInNewRound, BalanceCalc
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс ЩИТОВ ==========================
@router.callback_query(lambda c: c.data == 'main_shield', CountryStates.main_keyboard)
async def shield_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']}💲\n\n" \
                    f"🛡️<b>Щиты</b>🛡️\n" \
                    f"<b>300$</b>\n\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🛡️ Щит: {'✔️' if city['shieldInfo'] else '❌'} ---> " \
                         f"{'✔️' if city['shield'] or city['shieldInfo'] else '❌'}\n\n"
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Shield_TrueFalse(city_Info)
    )


@router.callback_query(lambda c: c.data.startswith("city_shield_"), CountryStates.main_keyboard)
async def callback_city_shield(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    split_callback_data = call.data.split('_')
    city_id = int(split_callback_data[2])
    selected_cities_shield = user_data.get('selectedShield')
    if selected_cities_shield is not None:
        selected_cities_shield = user_data['selectedShield']
    else:
        selected_cities_shield = []
        # for fCity in country_Info['friendlyCities']:
        #     if fCity['shieldInfo'] is True:
        #         selected_cities_shield.append(fCity)
    for city in city_Info:
        if city["cityId"] == city_id and city['shield'] is False:
            country_Info['balanceInfo'] -= 300
            city['shield'] = True
            selected_cities_shield.append(city)
            await call.answer(
                text=f"Поставлен щит на город {city['title']}"
            )
        if city["cityId"] == city_id and city['shield'] is True:
            country_Info['balanceInfo'] += 300
            city['shield'] = False
            selected_cities_shield.remove(city)
            await call.answer(
                text=f"Убран щит на город {city['title']}"
            )
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n{country_Info['title']}\n" \
                    f"💸{country_Info['balanceInfo']} 💲\n\n" \
                    f"🛡️<b>Щиты</b>🛡️\n" \
                    f"<b>300 💲</b>\n\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🛡️ Щит: {'✔️ ' if city['shieldInfo'] else '❌'} ---> " \
                         f"{'✔️' if city['shield'] or city['shieldInfo'] else '❌'}\n\n"

    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Shield_TrueFalse(city_Info)
    )
    await state.update_data(selectedShield=selected_cities_shield)


# ======================================= BACK TO MENU =======================
@router.callback_query(lambda c: c.data == "shield_menu", CountryStates.main_keyboard)
async def callback_shield_back_to_menu(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    world = user_data['world']
    ecology = world['ecology']
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    city_Info = country_Info['friendlyCities']
    rockets = RocketCalc(country_Info)
    incomeBalance = BalanceInNewRound(country_Info, ecology)
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    averageLifeStandardList = []
    for c in city_Info:
        averageLifeStandardList.append(c['lifestandard'])
    textForEdited = f"🌍 Мир 🌍\n" \
                    f"{world['title']}\n\n" \
                    f"🌱 Экология: <b>{round(ecology, 2)} %</b>\n\n" \
                    f"🗺️ Страна 🗺️\n" \
                    f"<b>{country_Info['title']}</b>\n\n" \
                    f"💸 Баланс: <b>{country_Info['balanceInfo']}</b> $ (+<b>{round(incomeBalance)}</b> $)\n" \
                    f"🚀 Ракет: <b>{rockets}</b> | {country_Info['rocket']}\n" \
                    f"🌿 Ур. жизни: <b>{round(sum(averageLifeStandardList)*ecology/400)}</b> %\n\n" \
                    f"🏙️ Города 🏙️\n"
    for city in city_Info:
        textForEdited += f"<b>{city['title'] if city['condition'] else '<s>' + city['title'] + '</s>'}</b>\n" \
                         f"🌿 Развитие: {str(city['lifestandard']) + ' + 20 ' if city['development'] else city['lifestandard']} %\n" \
                         f"🛡️ Щит: {'✔️ ' if city['shieldInfo'] else '❌'} ---> " \
                         f"{'✔️' if city['shield'] or city['shieldInfo'] else '❌'}\n\n"
    textForEdited += "<i>Ведущий сообщит Вам об окончании раунда, пожалуйста нажмите кнопку <b>Обновить</b> " \
                     "после завершения раунда</i>"
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Main_Keyboard()
    )
