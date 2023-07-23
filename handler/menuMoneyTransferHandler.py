from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from buttons.inlinebuttons.FormMainButton import in_Form_MoneyTransfer
from methods import ReCalcBalance
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс ПЕРЕВОД ДЕНЕГ ==========================
@router.callback_query(lambda c: c.data == 'main_moneyTransfer', CountryStates.main_keyboard)
async def moneyTransfer_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 Баланс: {country_Info['balanceInfo']} 💲\n\n" \
                    f"💰<b>Перевод денег</b>💰\n\n"
    for enemyCountry in country_Info['enemyCountries']:
        textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                         f"Перевод: {enemyCountry['moneyTransfer']} $\n\n"
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_MoneyTransfer(country_Info['enemyCountries'])
    )


# country_moneytransfer_
@router.callback_query(lambda c: c.data.startswith('country_moneytransfer_'), CountryStates.main_keyboard)
async def money_choose_enemy_country_transfer_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    split_callback_data = call.data.split('_')
    country_id_for_transfer = int(split_callback_data[2])
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 Баланс: {country_Info['balanceInfo']} 💲\n\n" \
                    f"💰<b>Перевод денег</b>💰\n\n"
    country_title_for_transfer = ""
    countryIdTransferList = user_data.get('countryIdMoneyTransfer')
    if countryIdTransferList is not None:
        countryIdTransferList = user_data['countryIdMoneyTransfer']
    else:
        countryIdTransferList = []
    for enemyCountry in country_Info['enemyCountries']:
        textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                         f"Перевод: {enemyCountry['moneyTransfer']} $\n\n"
        if enemyCountry['countryId'] == country_id_for_transfer:
            country_title_for_transfer = enemyCountry['title']
            countryIdTransferList.append(country_id_for_transfer)
    textForEdited += f"<i>Введите сумму для перевода средств в страну:<b> {country_title_for_transfer}</b></i>"
    await state.update_data(countryIdMoneyTransfer=countryIdTransferList)
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML
    )


@router.message(F.text.regexp(r'\d+'), CountryStates.main_keyboard)
async def message_money_transfer(message: Message, state: CountryStates.main_keyboard):
    if message.text.isdigit():
        user_data = await state.get_data()
        getFormCountry = user_data['form']
        country_Info = getFormCountry['form']
        selected_country_id_transfer = user_data.get('countryIdMoneyTransfer')
        if selected_country_id_transfer is not None:
            selected_country_id_transfer = user_data['countryIdMoneyTransfer']
            for eCountry in country_Info['enemyCountries']:
                for idECountry in selected_country_id_transfer:
                    if eCountry['countryId'] == idECountry:
                        eCountry['moneyTransfer'] = int(message.text)
            country_Info['balanceInfo'] -= int(message.text)
            ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
            textForEdited = f"🗺️ Страна 🗺️\n" \
                            f"{country_Info['title']}\n\n" \
                            f"💸 Баланс: {country_Info['balanceInfo']} 💲\n\n" \
                            f"💰<b>Перевод денег</b>💰\n\n"
            for enemyCountry in country_Info['enemyCountries']:
                textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                                 f"Перевод: {enemyCountry['moneyTransfer']} $\n\n"
            await message.answer(
                text=textForEdited,
                parse_mode=ParseMode.HTML,
                reply_markup=in_Form_MoneyTransfer(country_Info['enemyCountries'])
            )


# ============================= Очистка переводов ==============
# moneyTransfer_clear
@router.callback_query(lambda c: c.data == 'moneyTransfer_clear', CountryStates.main_keyboard)
async def clear_moneyTransfer_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    clear_transfer_selected = user_data.get('countryIdMoneyTransfer')
    if clear_transfer_selected is not None:
        clear_transfer_selected = user_data['countryIdMoneyTransfer']
        amount_transfer_balance = 0
        for eCountry in country_Info['enemyCountries']:
            amount_transfer_balance += eCountry['moneyTransfer']
            eCountry['moneyTransfer'] = 0
            for eCountryClear in clear_transfer_selected:
                if eCountry['countryId'] == eCountryClear:
                    clear_transfer_selected.remove(eCountryClear)
        country_Info['balanceInfo'] += amount_transfer_balance
        await call.answer(
            text="Очистка прошла успешно"
        )
    else:
        await call.answer(
            text="Что-то пошло не так, Очистка прошла успешно"
        )
    ReCalcBalance.BalanceCalc(country_Info, getFormCountry['countryInfo']['balance'])
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 Баланс: {country_Info['balanceInfo']} 💲\n\n" \
                    f"💰<b>Перевод денег</b>💰\n\n"
    for enemyCountry in country_Info['enemyCountries']:
        textForEdited += f"<b>{enemyCountry['title']}</b>\n" \
                         f"Перевод: {enemyCountry['moneyTransfer']} $\n\n"
    await call.message.edit_text(
        text=textForEdited,
        inline_message_id=call.inline_message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=in_Form_MoneyTransfer(country_Info['enemyCountries'])
    )
