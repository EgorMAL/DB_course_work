import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

AVALIABLE_MENUS_PRODUCTS = tp.Literal["menu", "delete_product", "add_product", "back"]

class ProductsMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS_PRODUCTS = "menu"

def products_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🗑️ Удалить пакет минут",
            callback_data=ProductsMenuCallback(next_menu_prefix="delete_product").pack()
        ),
        types.InlineKeyboardButton(
            text="🕒 Добавить пакет минут",
            callback_data=ProductsMenuCallback(next_menu_prefix="add_product").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=ProductsMenuCallback(next_menu_prefix="back").pack()
        )
    )
    return builder.as_markup()