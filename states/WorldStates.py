from aiogram.fsm.state import StatesGroup, State


class WorldStates(StatesGroup):
    after_choose_world = State()
    country = State()


class CountryStates(StatesGroup):
    password = State()
