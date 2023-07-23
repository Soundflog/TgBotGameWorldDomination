from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import requests as r

from buttons.inlinebuttons.chooseWorld import in_World_menu, in_Player_or_Curator
from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD
from states.WorldStates import WorldStates, PlayersStates

router = Router()


# router.message.middleware(WeekendCallbackMiddleware())
# router.callback_query.middleware(WeekendCallbackMiddleware())

# world_
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
        # reply_markup=in_Player_or_Curator()
        reply_markup=in_World_menu(world['id'])
    )


# @router.callback_query(lambda c: c.data == "player", WorldStates.after_choose_world)
# async def player_callback(call: CallbackQuery, state: WorldStates.after_choose_world):
#     await call.message.edit_reply_markup()
#     await call.message.edit_text(
#         text="Вы присоединились в игру как игрок",
#         inline_message_id=call.inline_message_id,
#         reply_markup=in_World_menu(world['id'])
#     )
#
#
# @router.callback_query(lambda c: c.data == "curator")
# async def curator_callback(call: CallbackQuery, state: FSMContext):
#     await call.message.edit_reply_markup()
#     await state.set_state(PlayersStates.curator)
#     await call.message.edit_text(
#         text="Вы присоединились в игру как игрок",
#         inline_message_id=call.inline_message_id,
#         reply_markup=in_Choose_World()
#     )
