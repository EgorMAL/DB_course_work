import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

AVALIABLE_MENUS_USERS = tp.Literal["menu", "delete_user", "add_user", "back"]

class UsersMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS_USERS = "menu"

def users_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🗑️ Удалить пользователя",
            callback_data=UsersMenuCallback(next_menu_prefix="delete_user").pack()
        ),
        types.InlineKeyboardButton(
            text="👤 Добавить пользователя",
            callback_data=UsersMenuCallback(next_menu_prefix="add_user").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=UsersMenuCallback(next_menu_prefix="back").pack()
        )
    )
    return builder.as_markup()