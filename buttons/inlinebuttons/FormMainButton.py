from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests as r

from config.configurations import REQUEST_URL_GAME, REQUEST_URL_WORLD


def in_Form_Main_Keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Развить города", callback_data="main_development"),
        InlineKeyboardButton(text="Поставить щит", callback_data="main_shield"),
        InlineKeyboardButton(text="Ядерная программа", callback_data="main_nuclearProgram"),
        InlineKeyboardButton(text="Экология", callback_data="main_ecology"),
        InlineKeyboardButton(text="Подвердить", callback_data="main_access"),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def in_Form_Development_TrueFalse(city_info):
    keyboard = InlineKeyboardBuilder()
    for i, city in enumerate(city_info):
        if city['condition'] is True:
            keyboard.add(
                InlineKeyboardButton(text=f'{city["title"]}', callback_data=f"city_development_{city['cityId']}")
            )
    keyboard.add(
        InlineKeyboardButton(text='<< Меню', callback_data="dev_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


class DevelopmentCallbackFactory(CallbackData, prefix="devnum"):
    action: str
    value: Optional[int]


def in_Form_Development(city_info):
    # buttonsKeyboard = [
    #     [
    #         InlineKeyboardButton(text="-1", callback_data="city_0_decr"),
    #         InlineKeyboardButton(text=f"{city_info[0]['title']}", callback_data="city_title_0"),
    #         InlineKeyboardButton(text="+1", callback_data="city_0_incr")
    #     ],
    #     [
    #         InlineKeyboardButton(text="-1", callback_data="city_1_decr"),
    #         InlineKeyboardButton(text=f"{city_info[1]['title']}", callback_data="city_title_1"),
    #         InlineKeyboardButton(text="+1", callback_data="city_1_incr")
    #     ],
    #     [
    #         InlineKeyboardButton(text="-1", callback_data="city_2_decr"),
    #         InlineKeyboardButton(text=f"{city_info[2]['title']}", callback_data="city_title_2"),
    #         InlineKeyboardButton(text="+1", callback_data="city_2_incr")
    #     ],
    #     [
    #         InlineKeyboardButton(text="-1", callback_data="city_3_decr"),
    #         InlineKeyboardButton(text=f"{city_info[3]['title']}", callback_data="city_title_3"),
    #         InlineKeyboardButton(text="+1", callback_data="city_3_incr")
    #     ],
    # ]
    # builder = InlineKeyboardBuilder()
    # buttonsKeyboard = [[], [], [], []]
    # for i, (city, button) in enumerate(zip(city_info, buttonsKeyboard)):
    #     button.append(
    #         InlineKeyboardButton(text="-1", callback_data=f"city_decr_{i}")
    #     )
    #     button.append(
    #         InlineKeyboardButton(text=f"{city['title']}", callback_data=f"city_title_{i}")
    #     )
    #     button.append(
    #         InlineKeyboardButton(text="+1", callback_data=f"city_decr_{i}"),
    #     )
    #     if i == 3:
    #         button.append(
    #             InlineKeyboardButton(text="Подвердить", callback_data=f"city_accept"),
    #         )
    #     builder.add(button[i])
    #
    # builder = InlineKeyboardBuilder()
    # builder.button(
    #     text="-1", callback_data=DevelopmentCallbackFactory(action="change", value=-1)
    # )
    # builder.button(
    #     text="-1", callback_data=DevelopmentCallbackFactory(action="title", value=city_info[0]['title'])
    # )
    # builder = InlineKeyboardBuilder()
    # for i, (b, city) in enumerate(zip(builder, city_info)):
    #     b(
    #         text="-1", callback_data=DevelopmentCallbackFactory(action="change", value=-1)
    #     )
    #     b(
    #         text=f"{city['title']}", callback_data=DevelopmentCallbackFactory(action="title")
    #     )
    #     b(
    #         text="+1", callback_data=DevelopmentCallbackFactory(action="change", value=+1)
    #     )
    builder = InlineKeyboardBuilder()
    for i, city in enumerate(city_info):
        builder.button(
            text="-1", callback_data=DevelopmentCallbackFactory(action="change", value=-1)
        )
        builder.button(
            text=f"{city['title']}", callback_data=DevelopmentCallbackFactory(action="nothing")
        )
        builder.button(
            text="+1", callback_data=DevelopmentCallbackFactory(action="change", value=+1)
        )
    builder.button(
        text="Подвердить", callback_data=DevelopmentCallbackFactory(action="finish")
    )

    builder.adjust(3)
    return builder.as_markup()
