from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import requests as r

from buttons.inlinebuttons.chooseWorld import in_World_menu
from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD
from states.WorldStates import WorldStates

router = Router()


# router.message.middleware(WeekendCallbackMiddleware())
# router.callback_query.middleware(WeekendCallbackMiddleware())


@router.callback_query(lambda c: c.data.startswith('world_'))
async def update_keyboard_worlds(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    split_callback_data = callback_query.data.split('_')
    world_id = split_callback_data[1]
    world = r.get(f"{REQUEST_URL_WORLD}/world?worldId={world_id}").json()['worldInfo']
    # worlds = r.get(f"{REQUEST_URL_GAME}/worlds").json()
    await state.set_state(WorldStates.after_choose_world)

    await state.update_data(world=world)

    await callback_query.message.edit_text(
        text=f"🌍 Мир 🌍\n"
             f"{world['title']}\n\n"
             f"🗺️ Выберите страну",
        inline_message_id=callback_query.inline_message_id,
        reply_markup=in_World_menu(world['id'])
    )


