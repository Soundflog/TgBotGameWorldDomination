from contextlib import suppress

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Nuclear_TrueFalse, \
    in_Form_Bomb_Enemy, in_Form_Bomb_Enemy_Cities
from methods import ReCalcBalance
from methods.ReCalcBalance import RocketCalc, BalanceCalc
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс ЯДЕРНОЙ ПРОГРАММЫ ==========================
@router.callback_query(lambda c: c.data == 'main_nuclearProgram', CountryStates.main_keyboard)
async def nuclear_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    rockets = RocketCalc(country_Info)
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"☢️<b>Ядерная программа</b>☢️\n" \
                    f"Цены: \n" \
                    f"Развитие --- <b> 500 💲</b>\n" \
                    f"Ракета --- <b> 150 💲</b>\n\n"
    textForEdited += f"Развита ядерная программа: {'✔️' if country_Info['nuclearProgramInfo'] else '❌'} " \
                     f"---> {'✔️' if country_Info['nuclearProgram'] else '❌'}\n" \
                     f"Ракет: {rockets} ---> {country_Info['rocket']}"
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Nuclear_TrueFalse(country_Info)
    )


# ========================================== РАЗВИТЬ ЯДЕРНУЮ =============================
@router.callback_query(lambda c: c.data == "rocket_development", CountryStates.main_keyboard)
async def callback_nuclear_development(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    # Nuclear Program
    if country_Info['nuclearProgram'] is False:
        country_Info['nuclearProgram'] = True
        country_Info['balanceInfo'] -= 500
    else:
        country_Info['nuclearProgram'] = False
        country_Info['balanceInfo'] += 500

    rockets = RocketCalc(country_Info)
    BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"☢️<b>Ядерная программа</b>☢️\n" \
                    f"Цены: \n" \
                    f"Развитие --- <b> 500 💲</b>\n" \
                    f"Ракета --- <b> 150 💲</b>\n\n"
    textForEdited += f"Развитие ядерной программы: {'✔️' if country_Info['nuclearProgramInfo'] else '❌'} " \
                     f"---> {'✔️' if country_Info['nuclearProgram'] else '❌'}\n" \
                     f"Ракет: {rockets} ---> {country_Info['rocket']}"
    # {'✔️' if city['shieldInfo'] else '❌'} ---> {'✔️' if city['shield'] else '❌'}
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Nuclear_TrueFalse(country_Info)
    )


# ============================================ ПРОИЗВЕСТИ РАКЕТУ ===================
@router.callback_query(lambda c: c.data == "rocket_add", CountryStates.main_keyboard)
async def callback_nuclear_add(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    # Nuclear Program
    if country_Info['nuclearProgram'] is False:
        await call.answer(
            text="Пожалуйста подождите пока развивается ядерная программа\n"
                 "Развитие ядерной программы 1 раунд",
            show_alert=True
        )
    count_rocket_add = user_data.get('selectedRocketAdd')
    if count_rocket_add is not None:
        count_rocket_add = user_data['selectedRocketAdd']
    else:
        count_rocket_add = country_Info['rocket']
    if country_Info['nuclearProgramInfo'] is True and count_rocket_add < 3:
        country_Info['rocket'] += 1
        country_Info['balanceInfo'] -= 150
        count_rocket_add += 1
        await call.answer(
            text="+1 Ракета"
        )
        rockets = RocketCalc(country_Info)
        textForEdited = f"🗺️ Страна 🗺️\n" \
                        f"{country_Info['title']}\n" \
                        f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                        f"☢️<b>Ядерная программа</b>☢️\n" \
                        f"Цены: \n" \
                        f"Развитие --- <b> 500 💲</b>\n" \
                        f"Ракета --- <b> 150 💲</b>\n\n"
        textForEdited += f"Развита ядерная программа: " \
                         f"{'✔️' if country_Info['nuclearProgramInfo'] else '❌'} ---> " \
                         f"{'✔️' if country_Info['nuclearProgram'] else '❌'}\n" \
                         f"Ракет: {rockets} ---> {country_Info['rocket']}"
        await call.message.edit_text(
            text=textForEdited,
            parse_mode=ParseMode.HTML,
            inline_message_id=call.inline_message_id,
            reply_markup=in_Form_Nuclear_TrueFalse(country_Info)
        )
        await state.update_data(selectedRocketAdd=count_rocket_add)
    else:
        await call.answer(
            text="Не больше 3 ракет за раунд"
        )


# ========================================= УБРАТЬ РАКЕТУ =========================
@router.callback_query(lambda c: c.data == "rocket_remove", CountryStates.main_keyboard)
async def callback_nuclear_remove(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    # Nuclear Program
    if country_Info['nuclearProgram'] is False:
        await call.answer(
            text="Пожалуйста подождите пока развивается ядерная программа\n"
                 "Развитие ядерной программы 1 раунд",
            show_alert=True
        )
    count_rocket_add = user_data.get('selectedRocketAdd')
    if count_rocket_add is not None:
        count_rocket_add = user_data['selectedRocketAdd']
    else:
        count_rocket_add = country_Info['rocket']
    if country_Info['nuclearProgramInfo'] is True and 3 > count_rocket_add > 0:
        country_Info['rocket'] -= 1
        country_Info['balanceInfo'] += 150
        count_rocket_add -= 1
        await call.answer(
            text="-1 Ракета"
        )
        ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
        rockets = RocketCalc(country_Info)
        textForEdited = f"🗺️ Страна 🗺️\n" \
                        f"{country_Info['title']}\n" \
                        f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                        f"☢️<b>Ядерная программа</b>☢️\n" \
                        f"Цены: \n" \
                        f"Развитие --- <b> 500 💲</b>\n" \
                        f"Ракета --- <b> 150 💲</b>\n\n"
        textForEdited += f"Развита ядерная программа: " \
                         f"{'✔️' if country_Info['nuclearProgramInfo'] else '❌'} ---> " \
                         f"{'✔️' if country_Info['nuclearProgram'] else '❌'}\n" \
                         f"Ракет: {rockets} ---> {country_Info['rocket']}"

        await call.message.edit_text(
            text=textForEdited,
            parse_mode=ParseMode.HTML,
            inline_message_id=call.inline_message_id,
            reply_markup=in_Form_Nuclear_TrueFalse(country_Info)
        )
        await state.update_data(selectedRocketAdd=count_rocket_add)
    else:
        await call.answer(
            text="Нельзя убрать меньше 0"
        )


# ========================================= БОМБИТЬ =========================
@router.callback_query(lambda c: c.data == "rocket_bomb", CountryStates.main_keyboard)
async def callback_nuclear_bomb(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    rockets = RocketCalc(country_Info)
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"☢️<b>Ядерная программа</b>☢️\n" \
                    f"Цены: \n" \
                    f"Развитие --- <b> 500 💲</b>\n" \
                    f"Ракета --- <b> 150 💲</b>\n\n"
    textForEdited += f"Развита ядерная программа: " \
                     f"{'✔️' if country_Info['nuclearProgramInfo'] else '❌'} ---> " \
                     f"{'✔️' if country_Info['nuclearProgram'] else '❌'}\n" \
                     f"Ракет: {rockets} + {country_Info['rocket']}\n\n" \
                     f"<i>Кол-во ракет считается: кол-во ракет с прошлого раунда + кол-во ракет в производстве</i>"

    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_Bomb_Enemy(country_Info['enemyCountries'])
    )


# =================================== ВЫБОР КАКУЮ СТРАНУ БОМБИТЬ ==================
@router.callback_query(lambda c: c.data.startswith("country_bomb_"), CountryStates.main_keyboard)
async def callback_nuclear_bomb_to_country(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    split_callback_data = call.data.split('_')
    country_id_for_bomb = int(split_callback_data[2])
    enemy_Countries = country_Info['enemyCountries']
    textForEdited = "Произошла ошибка"
    enemy_cities = []
    rockets = RocketCalc(country_Info)
    for enemyCountry in enemy_Countries:
        if enemyCountry['countryId'] == country_id_for_bomb:
            textForEdited = f"💥 БОМБИТЬ 💥\n" \
                            f"<b>{enemyCountry['title']}</b>\n" \
                            f"🚀 Кол-во ракет: {rockets}\n\n" \
                            f"🏙️ ГОРОДА 🏙️\n"
            for enemyCity in enemyCountry['enemyCities']:
                enemy_cities.append(enemyCity)
                textForEdited += f"<b>{enemyCity['title'] if enemyCity['condition'] else '<s>' + enemyCity['title'] + '</s>'}</b>\n" \
                                 f"🌿 Ур. жизни: {enemyCity['lifestandard']} %\n" \
                                 f"💣 Отправлена бомба: {'✔️' if enemyCity['bomb'] else '❌'}\n\n"

    await state.update_data(country_id_for_bomb=country_id_for_bomb)
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Bomb_Enemy_Cities(enemy_cities)
    )
    await call.answer()


# =================================== БОМБИТЬ ГОРОД ==================
@router.callback_query(lambda c: c.data.startswith("city_bomb_"), CountryStates.main_keyboard)
async def callback_nuclear_bomb_to_city(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    split_callback_data = call.data.split('_')
    city_id_for_bomb = int(split_callback_data[2])
    enemy_Countries = country_Info['enemyCountries']
    enemy_cities = []
    enemyCountryById = {}
    for enemyCountry in enemy_Countries:
        if enemyCountry['countryId'] == user_data['country_id_for_bomb']:
            enemyCountryById.update(enemyCountry)
            for city_enemy in enemyCountry['enemyCities']:
                if city_enemy['cityId'] == city_id_for_bomb:
                    if city_enemy['bomb'] is False:
                        city_enemy['bomb'] = True
                    elif city_enemy['bomb'] is True:
                        city_enemy['bomb'] = False
                enemy_cities.append(city_enemy)
    rockets = RocketCalc(country_Info)
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    txtForEdited = f"💥 БОМБИТЬ 💥\n" \
                   f"<b>{enemyCountryById['title']}</b>\n\n" \
                   f"🚀 Кол-во ракет: {rockets}\n\n" \
                   f"🏙️ ГОРОДА 🏙️\n"
    for eCity in enemy_cities:
        txtForEdited += f"<b>{eCity['title'] if eCity['condition'] else '<s>' + eCity['title'] + '</s>'}</b>\n" \
                        f"🌿 Ур. жизни: {eCity['lifestandard']} %\n" \
                        f"💣 Отправлена бомба: {'✔️' if eCity['bomb'] else '❌'}\n\n"
    await call.answer(
        text=f"Ракет: {rockets}"
    )
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            text=txtForEdited,
            inline_message_id=call.inline_message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=in_Form_Bomb_Enemy_Cities(enemy_cities)
        )
