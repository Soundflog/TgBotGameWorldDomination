from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def in_Form_Main_Keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🌿 Развить города 🌿", callback_data="main_development"),
        InlineKeyboardButton(text="🛡️ Поставить щит 🛡️", callback_data="main_shield"),
        InlineKeyboardButton(text="☢️ Ядерная программа ☢️", callback_data="main_nuclearProgram"),
        InlineKeyboardButton(text="🌱 Экология 🌱", callback_data="main_ecology"),
        InlineKeyboardButton(text="✅ Подвердить ✅", callback_data="main_access"),
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


def in_Form_Shield_TrueFalse(city_info):
    keyboard = InlineKeyboardBuilder()
    for i, city in enumerate(city_info):
        if city['condition'] is True and city['shieldInfo'] is False:
            keyboard.add(
                InlineKeyboardButton(text=f"{city['title']}", callback_data=f"city_shield_{city['cityId']}")
            )
    keyboard.add(
        InlineKeyboardButton(text='<< Меню', callback_data="shield_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def in_Form_Nuclear_TrueFalse(formRound):
    keyboard = InlineKeyboardBuilder()
    if formRound['nuclearProgramInfo'] is True:
        keyboard.add(
            InlineKeyboardButton(text="Произвести ракету", callback_data="rocket_add")
        )
        keyboard.add(
            InlineKeyboardButton(text="Убрать ракету", callback_data="rocket_remove")
        )
        keyboard.add(
            InlineKeyboardButton(text="Бомбить", callback_data="rocket_bomb")
        )
    else:
        keyboard.add(
            InlineKeyboardButton(text="Развить ядерную программу", callback_data="rocket_development")
        )
    keyboard.add(
        InlineKeyboardButton(text="<< Меню", callback_data="shield_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def in_Form_Bomb_Enemy(enemyCountries):
    keyboard = InlineKeyboardBuilder()
    for enemy in enemyCountries:
        keyboard.add(
            InlineKeyboardButton(text=f"{enemy['title']}", callback_data=f"country_bomb_{enemy['countryId']}")
        )
    keyboard.add(
        InlineKeyboardButton(text="<< Меню", callback_data="shield_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def in_Form_Bomb_Enemy_Cities(enemyCities):
    keyboard = InlineKeyboardBuilder()
    for enemy in enemyCities:
        if enemy['condition']:
            keyboard.add(
                InlineKeyboardButton(text=f"{enemy['title']}", callback_data=f"city_bomb_{enemy['cityId']}")
            )
    keyboard.add(
        InlineKeyboardButton(text="<< Меню", callback_data="shield_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
