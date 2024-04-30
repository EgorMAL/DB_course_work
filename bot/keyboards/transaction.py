import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

AVALIABLE_MENUS_TRANSACTION = tp.Literal["menu", "add_transaction", "back"]

class TransactionCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS_TRANSACTION = "menu"

def transaction_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="💸 Добавить транзакцию",
            callback_data=TransactionCallback(next_menu_prefix="add_transaction").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=TransactionCallback(next_menu_prefix="back").pack()
        )
    )
    return builder.as_markup()