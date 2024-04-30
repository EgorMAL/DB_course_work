import typing as tp
from aiogram import types

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

AVALIABLE_MENUS = tp.Literal["menu", "users", "products", "market", "booking", "transaction"]

class MainMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS = "menu"

def menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🧑‍💻 Пользователи",
            callback_data=MainMenuCallback(next_menu_prefix="users").pack()
        ),
        types.InlineKeyboardButton(
            text="🕒 Пакеты минут",
            callback_data=MainMenuCallback(next_menu_prefix="products").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🛒 Магазин",
            callback_data=MainMenuCallback(next_menu_prefix="market").pack()
        ),
        types.InlineKeyboardButton(
            text="📅 Бронирование",
            callback_data=MainMenuCallback(next_menu_prefix="booking").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="💸 Транзакции",
            callback_data=MainMenuCallback(next_menu_prefix="transaction").pack()
        )
    )
    return builder.as_markup()