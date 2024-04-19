from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from buttons.inlinebuttons.chooseWorld import in_Choose_World

# from Middleware.midle_ware import WeekendMessageMiddleware

router = Router()


# router.message.middleware(WeekendMessageMiddleware())


@router.message(Command(commands=["start"]))
async def start(message: Message):
    user_id = message.from_user.id

    # проверка на админа
    # if user_id in admins:
    await message.answer(text="ДОБРО ПОЖАЛОВАТЬ В ИГРУ \n\n🌍 <b>МИРОВОЕ ГОСПОДСТВО</b> 🌍\n\n"
                              "<i>Выберите <b>МИР</b> для подключения</i>",
                         parse_mode=ParseMode.HTML,
                         reply_markup=in_Choose_World())

