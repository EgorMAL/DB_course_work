import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

AVALIABLE_MENUS_RESERVATIONS = tp.Literal["menu", "add_reservation", "back"]

class ReservationsMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS_RESERVATIONS = "menu"

def reservations_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📅 Добавить бронь",
            callback_data=ReservationsMenuCallback(next_menu_prefix="add_reservation").pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=ReservationsMenuCallback(next_menu_prefix="back").pack()
        )
    )
    return builder.as_markup()