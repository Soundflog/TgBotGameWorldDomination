from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests as r

from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD


def in_Player_or_Curator():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Игрок", callback_data="player"),
        InlineKeyboardButton(text="Ведущий", callback_data="curator")
    )
    keyboard.adjust(2)
    return keyboard.as_markup()


def in_Choose_World():
    keyboard = InlineKeyboardBuilder()
    worlds = r.get(f"{REQUEST_URL_GAME}/worlds").json()
    for world in worlds['worlds']:
        print(f"world = {world}")
        keyboard.add(
            InlineKeyboardButton(text=f"{world['title']}", callback_data=f"world_{world['id']}")
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def in_World_menu(worldId: int):
    keyboard_markup = InlineKeyboardBuilder()
    worldById = r.get(f"{REQUEST_URL_WORLD}/world?worldId={worldId}").json()
    for country in worldById['worldInfo']['countryInfos']:
        keyboard_markup.add(
            InlineKeyboardButton(text=f"{country['title']}", callback_data=f"country_{country['id']}")
        )
    keyboard_markup.adjust(1)
    return keyboard_markup.as_markup()
