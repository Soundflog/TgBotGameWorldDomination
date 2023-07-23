from contextlib import suppress

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from buttons.inlinebuttons.FormMainButton import in_Form_Ecology
from states.WorldStates import CountryStates

router = Router()


# ============================ Стартовое смс Ecology ==========================
@router.callback_query(lambda c: c.data == 'main_ecology', CountryStates.main_keyboard)
async def ecology_menu_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    await call.message.edit_reply_markup()
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    ecology = user_data['world']['ecology']
    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"🌱<b>Экология</b>🌱\n" \
                    f"{round(ecology, 2)}\n\n" \
                    f"Цены: \n" \
                    f"Экология x1 --- <b> 150 💲</b>\n" \
                    f"Экология x2 --- <b> 300 💲</b>\n" \
                    f"Экология x3 --- <b> 450 💲</b>\n\n" \
                    f"Кол-во вложений в экологию: {country_Info['ecology']}"
    await call.message.edit_text(
        text=textForEdited,
        parse_mode=ParseMode.HTML,
        inline_message_id=call.inline_message_id,
        reply_markup=in_Form_Ecology()
    )


@router.callback_query(lambda c: c.data == "ecology_add", CountryStates.main_keyboard)
async def ecology_x_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    ecology = user_data['world']['ecology']
    ecology_list = user_data.get('ecology_x')
    if ecology_list is not None:
        ecology_list = user_data['ecology_x']
    else:
        ecology_list = []
    if len(ecology_list) == 0:
        # Список пуст
        ecology_list.append(1)
        country_Info['ecology'] += 1
        country_Info['balanceInfo'] -= 150
    else:
        if len(ecology_list) >= 3:
            await call.answer(
                text="Больше 3 раз вложиться нельзя"
            )
        else:
            ecology_list.append(1)
            country_Info['ecology'] = len(ecology_list)
            country_Info['balanceInfo'] -= 150

    textForEdited = f"🗺️ Страна 🗺️\n" \
                    f"{country_Info['title']}\n" \
                    f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                    f"🌱<b>Экология</b>🌱\n" \
                    f"{round(ecology, 2)}\n\n" \
                    f"Цены: \n" \
                    f"Экология x1 --- <b> 150 💲</b>\n" \
                    f"Экология x2 --- <b> 300 💲</b>\n" \
                    f"Экология x3 --- <b> 450 💲</b>\n\n" \
                    f"<i>Кол-во вложений в экологию: <b>{country_Info['ecology']}</b></i>"
    await state.update_data(ecology_x=ecology_list)
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            text=textForEdited,
            parse_mode=ParseMode.HTML,
            inline_message_id=call.inline_message_id,
            reply_markup=in_Form_Ecology()
        )


@router.callback_query(lambda c: c.data == "ecology_remove", CountryStates.main_keyboard)
async def ecology_remove_callback(call: CallbackQuery, state: CountryStates.main_keyboard):
    user_data = await state.get_data()
    getFormCountry = user_data['form']
    country_Info = getFormCountry['form']
    ecology = user_data['world']['ecology']
    ecology_list = user_data.get('ecology_x')
    if ecology_list is not None:
        ecology_list = user_data['ecology_x']
        amount_ecology = len(ecology_list)
        country_Info['balanceInfo'] += 150 * amount_ecology
        ecology_list = []
        country_Info['ecology'] = 0
        await call.answer(
            text="Очистка успешно"
        )
        textForEdited = f"🗺️ Страна 🗺️\n" \
                        f"{country_Info['title']}\n" \
                        f"💸 {country_Info['balanceInfo']} 💲\n\n" \
                        f"🌱<b>Экология</b>🌱\n" \
                        f"{round(ecology, 2)}\n\n" \
                        f"Цены: \n" \
                        f"Экология x1 --- <b> 150 💲</b>\n" \
                        f"Экология x2 --- <b> 300 💲</b>\n" \
                        f"Экология x3 --- <b> 450 💲</b>\n\n" \
                        f"Кол-во вложений в экологию: {country_Info['ecology']}"
        await state.update_data(ecology_x=ecology_list)
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                text=textForEdited,
                parse_mode=ParseMode.HTML,
                inline_message_id=call.inline_message_id,
                reply_markup=in_Form_Ecology()
            )
    else:
        await call.answer(
            text="Очищено: 0"
        )
