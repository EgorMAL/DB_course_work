import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

AVALIABLE_MENUS_MARKET = tp.Literal["menu", "delete_market", "add_market", "back"]

class MarketMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS_MARKET = "menu"

def market_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🗑️ Удалить товар",
            callback_data=MarketMenuCallback(next_menu_prefix="delete_market").pack()
        ),
        types.InlineKeyboardButton(
            text="🛒 Добавить товар",
            callback_data=MarketMenuCallback(next_menu_prefix="add_market").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=MarketMenuCallback(next_menu_prefix="back").pack()
        )
    )
    return builder.as_markup()
