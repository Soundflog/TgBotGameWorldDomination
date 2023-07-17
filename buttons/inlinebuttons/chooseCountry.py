from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests as r

from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD


def in_Choose_Country(countryId: int):
    keyboard = InlineKeyboardBuilder()
    worlds = r.get(f"{REQUEST_URL_GAME}/worlds").json()
    for world in worlds['worlds']:
        print(f"world = {world}")
        keyboard.add(
            InlineKeyboardButton(text=f"{world['title']}", callback_data=f"world_{world['id']}")
        )
    keyboard.adjust(1)
    return keyboard.as_markup()