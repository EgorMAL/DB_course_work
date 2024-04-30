from sys import prefix
import typing as tp
import asyncio

from aiogram import types, Router, F

from aiogram.filters import CommandStart, Command, or_f
from aiogram.filters.command import CommandObject
from aiogram.utils.markdown import hbold
import dotenv

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import gettext as _
import requests
from ..keyboards.menu import MainMenuCallback, menu_keyboard
from ..keyboards.users import UsersMenuCallback, users_menu_keyboard
from ..keyboards.products import ProductsMenuCallback, products_menu_keyboard
from ..keyboards.market import MarketMenuCallback, market_menu_keyboard
from ..keyboards.reservations import ReservationsMenuCallback, reservations_menu_keyboard
from ..keyboards.transaction import TransactionCallback, transaction_menu_keyboard

import os

router: tp.Final[Router] = Router(name="common")

dotenv.load_dotenv()

token = os.getenv("api_token")

headers = {
    "Authorization": f"Bearer {token}"
}
print(headers)
base_url = "https://biome-api.onixx.ru"

class AdminPanelStates(StatesGroup):
    """States for admin panel"""
    delete_user = State()
    add_user = State()
    add_product = State()
    delete_product = State()
    add_market = State()
    delete_market = State()
    add_reservation = State()
    add_transaction = State()

@router.message(CommandStart())
async def start(message: types.Message) -> None:
    """Home page, show aactive hosts and inline keyboard"""
    # get all hosts and show them
    response = requests.get(base_url + "/api/api/hosts", headers=headers)
    if response.status_code != 200:
        await message.answer("Ошибка при получении списка компов")
        print(response.json())
        return
    hosts = response.json()['result']
    # parse hosts reesponse
    hosts_text = ""
    for host in hosts:
        hosts_text += f"🖥️ {host['name']}"
        status = host['status']
        if status == "disabled":
            hosts_text += "❌ offline\n"
        elif status == "await":
            hosts_text += "⏳ online, waiting for player\n"
        else:
            hosts_text += "✅ playing\n"
    await message.answer(
       text="Добро подаловать в Biome Bot!\n\nСтатус компов:\n" + hosts_text,
        reply_markup=menu_keyboard()
    )

@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "users"))
async def users_menu(query: types.CallbackQuery) -> None:
    """Show users menu and list users"""
    users = requests.get(base_url + "/api/api/users", headers=headers).json()['result']
    users_text = ""
    for user in users:
        users_text += f"👤 {user['username']} ID: {user["id"]}\n"
        # parse name and email
        users_text += f"Имя: {user['name']}\n"
        users_text += f"Email: {user['email']}\n\n"

    await query.message.answer(
        text="Пользователи:\n" + users_text,
        reply_markup=users_menu_keyboard()
    )

@router.callback_query(UsersMenuCallback.filter(F.next_menu_prefix == "delete_user"))
async def delete_user(query: types.CallbackQuery, state: FSMContext) -> None:
    """Delete user by ID"""
    await query.message.answer("Введите ID пользователя, которого хотите удалить")
    await state.set_state(AdminPanelStates.delete_user)

@router.message(AdminPanelStates.delete_user)
async def delete_user_by_id(message: types.Message, state: FSMContext) -> None:
    """Delete user by ID"""
    user_id = message.text
    response = requests.delete(base_url + f"/api/api/users/{user_id}", headers=headers)
    if response.status_code == 200:
        await message.answer("Пользователь удалён")
    else:
        await message.answer("Ошибка при удалении пользователя")
    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(UsersMenuCallback.filter(F.next_menu_prefix == "add_user"))
async def add_user(query: types.CallbackQuery, state: FSMContext) -> None:
    """Add user"""
    await query.message.answer("Введите имя пользователя, пароль, номер телефона, email, адрес, город, страну, имя и фамилию через запятую")
    await state.set_state(AdminPanelStates.add_user)

@router.message(AdminPanelStates.add_user)
async def add_user_by_id(message: types.Message, state: FSMContext) -> None:
    """Add user by ID"""
    user_data = message.text.split(",")
    if len(user_data) != 9:
        await message.answer("Неверное количество аргументов")
        # show main menu
        await start(message)
        return
    user_data = {
        "username": user_data[0],
        "password": user_data[1],
        "phone": user_data[2],
        "email": user_data[3],
        "address": user_data[4],
        "city": user_data[5],
        "country": user_data[6],
        "name": user_data[7],
        "surname": user_data[8]
    }
    response = requests.post(base_url + "/api/api/users/create", headers=headers, json=user_data)
    if response.status_code == 201:
        await message.answer("Пользователь добавлен")
    else:
        await message.answer("Ошибка при добавлении пользователя")
    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(UsersMenuCallback.filter(F.next_menu_prefix == "back"))
async def back_to_main_menu(query: types.CallbackQuery) -> None:
    """Back to main menu"""
    await start(query.message)

@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "products"))
async def products_menu(query: types.CallbackQuery) -> None:
    """Show products menu and list products"""
    products = requests.get(base_url + "/api/api/products", headers=headers).json()['result']
    products_text = ""
    for product in products:
        products_text += f"🕒 {product['name']} ID: {product["id"]}\n"
        # parse data
        products_text += f"Количество секунд: {product['included_time']}\n"
        products_text += f"Время жизни пакета (сек): {product['lifetime']}\n"
        products_text += f"Ценообразование: {str(product['coast_sheme'])}\n"

    await query.message.answer(
        text="Пакеты минут:\n" + products_text,
        reply_markup=products_menu_keyboard()
    )

@router.callback_query(ProductsMenuCallback.filter(F.next_menu_prefix == "delete_product"))
async def delete_product(query: types.CallbackQuery, state: FSMContext) -> None:
    """Delete product by ID"""
    await query.message.answer("Введите ID пакета минут, который хотите удалить")
    await state.set_state(AdminPanelStates.delete_product)

@router.message(AdminPanelStates.delete_product)
async def delete_product_by_id(message: types.Message, state: FSMContext) -> None:
    """Delete product by ID"""
    product_id = message.text
    response = requests.delete(base_url + f"/api/api/products/{product_id}", headers=headers)
    if response.status_code == 200:
        await message.answer("Пакет минут удалён")
    else:
        await message.answer("Ошибка при удалении пакета минут")
    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(ProductsMenuCallback.filter(F.next_menu_prefix == "add_product"))
async def add_product(query: types.CallbackQuery, state: FSMContext) -> None:
    """Add product"""
    await query.message.answer("Введите имя пакета, количество секунд, время жизни пакета и ценообразование через запятую")
    await state.set_state(AdminPanelStates.add_product)

@router.message(AdminPanelStates.add_product)
async def add_product_by_id(message: types.Message, state: FSMContext) -> None:
    """Add product by ID"""
    product_data = message.text.split(",")
    if len(product_data) != 4:
        await message.answer("Неверное количество аргументов")
        # show main menu
        await start(message)
        return
    product_data = {
        "name": product_data[0],
        "included_time": product_data[1],
        "lifetime": product_data[2],
        "priority_level": 1,
        "available_options": {},
        "coast_sheme": {
        "profile": [
          { "price": product_data[3],
           "currency_id": 1
          },
          { "price": product_data[3],
           "currency_id": 2
          }
        ]
        }
    }
    response = requests.post(base_url + "/api/api/products/create", headers=headers, json=product_data)
    if response.status_code == 201:
        await message.answer("Пакет минут добавлен")
    else:
        await message.answer("Ошибка при добавлении пакета минут")

    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(ProductsMenuCallback.filter(F.next_menu_prefix == "back"))
async def back_to_main_menu_products(query: types.CallbackQuery) -> None:
    """Back to main menu"""
    await start(query.message)

@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "market"))
async def market_menu(query: types.CallbackQuery) -> None:
    """Show market menu and list products"""
    market = requests.get(base_url + "/api/api/market", headers=headers).json()['result']
    market_text = ""
    for product in market:
        market_text += f"🛒 {product['name']}\n"
        # parse data
        market_text += f"Категория: {product['category']}\n"
        market_text += f"Цена: {product['cost']}\n\n"

    await query.message.answer(
        text="Товары:\n" + market_text,
        reply_markup=market_menu_keyboard()
    )

@router.callback_query(MarketMenuCallback.filter(F.next_menu_prefix == "delete_market"))
async def delete_market(query: types.CallbackQuery, state: FSMContext) -> None:
    """Delete product by ID"""
    await query.message.answer("Введите имя товара, который хотите удалить")
    await state.set_state(AdminPanelStates.delete_market)

@router.message(AdminPanelStates.delete_market)
async def delete_market_by_id(message: types.Message, state: FSMContext) -> None:
    """Delete product by ID"""
    product_name = message.text
    response = requests.delete(base_url + f"/api/api/market/{product_name}", headers=headers)
    if response.status_code == 200:
        await message.answer("Товар удалён")
    else:
        await message.answer("Ошибка при удалении товара")
    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(MarketMenuCallback.filter(F.next_menu_prefix == "add_market"))
async def add_market(query: types.CallbackQuery, state: FSMContext) -> None:
    """Add product"""
    await query.message.answer("Введите имя товара, категорию, цену через запятую")
    await state.set_state(AdminPanelStates.add_market)

@router.message(AdminPanelStates.add_market)
async def add_market_by_id(message: types.Message, state: FSMContext) -> None:
    """Add product by ID"""
    product_data = message.text.split(",")
    if len(product_data) != 3:
        await message.answer("Неверное количество аргументов")
        # show main menu
        await start(message)
        return
    product_data = {
        "name": product_data[0],
        "category": product_data[1],
        "cost": product_data[2]
    }
    response = requests.post(base_url + "/api/api/market/create", headers=headers, json=product_data)
    if response.status_code == 201:
        await message.answer("Товар добавлен")
    else:
        await message.answer("Ошибка при добавлении товара")

    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(MarketMenuCallback.filter(F.next_menu_prefix == "back"))
async def back_to_main_menu_market(query: types.CallbackQuery) -> None:
    """Back to main menu"""
    await start(query.message)

@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "booking"))
async def booking_menu(query: types.CallbackQuery) -> None:
    """Show reservations menu and list reservations"""
    reservations = requests.get(base_url + "/api/api/reservations", headers=headers).json()['result']
    reservations_text = ""
    for reservation in reservations:
        reservations_text += f"📅 ID: {reservation["id"]}\n"
        # parse data
        reservations_text += f"Дата начала: {reservation['date_from']}\n"
        reservations_text += f"Дата окончания: {reservation['date_to']}\n"
        reservations_text += f"Компьютер: {reservation['host_id']}\n"
        reservations_text += f"Пользователь: {reservation['user_id']}\n\n"

    await query.message.answer(
        text="Брони:\n" + reservations_text,
        reply_markup=reservations_menu_keyboard()
    )

@router.callback_query(ReservationsMenuCallback.filter(F.next_menu_prefix == "add_reservation"))
async def add_reservation(query: types.CallbackQuery, state: FSMContext) -> None:
    """Add reservation"""
    await query.message.answer("Введите ID пользователя, ID компьютера, дату начала и дату окончания через запятую\nФормат даты: YYYY-MM-DDTHH:MM:SS.000Z")
    await state.set_state(AdminPanelStates.add_reservation)

@router.message(AdminPanelStates.add_reservation)
async def add_reservation_by_id(message: types.Message, state: FSMContext) -> None:
    """Add reservation by ID"""
    reservation_data = message.text.split(",")
    if len(reservation_data) != 4:
        await message.answer("Неверное количество аргументов")
        # show main menu
        await start(message)
        return
    reservation_data = {
        "user_id": reservation_data[0],
        "host_id": reservation_data[1],
        "date_from": reservation_data[2],
        "date_to": reservation_data[3]
    }
    response = requests.post(base_url + "/api/api/reservations/create", headers=headers, json=reservation_data)
    if response.status_code == 201:
        await message.answer("Бронь добавлена")
    else:
        await message.answer("Ошибка при добавлении брони")

    await state.clear()
    # show main menu
    await start(message)

@router.callback_query(ReservationsMenuCallback.filter(F.next_menu_prefix == "back"))
async def back_to_main_menu_reservations(query: types.CallbackQuery) -> None:
    """Back to main menu"""
    await start(query.message)

@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "transaction"))
async def transaction_menu(query: types.CallbackQuery) -> None:
    """Show transactions menu and list transactions"""
    transactions = requests.get(base_url + "/api/api/transactions", headers=headers).json()['result']
    transactions_text = ""
    for transaction in transactions:
        transactions_text += f"💸 ID: {transaction["id"]}\n"
        # parse data
        transactions_text += f"Дата: {transaction['date']}\n"
        transactions_text += f"Сумма: {transaction['summ']}\n"
        transactions_text += f"Пользователь: {transaction['user_id']}\n"
        transactions_text += f"Добавил админ с ID: {transaction['created_by_id']}\n"
        transactions_text += f"Тип: {transaction['type']}\n\n"

    await query.message.answer(
        text="Транзакции:\n" + transactions_text,
        reply_markup=transaction_menu_keyboard()
    )

@router.callback_query(TransactionCallback.filter(F.next_menu_prefix == "add_transaction"))
async def add_transaction(query: types.CallbackQuery, state: FSMContext) -> None:
    """Add transaction"""
    await query.message.answer("Введите ID пользователя, сумму и тип транзакции через запятую\nТипы транзакций: deposit, set")
    await state.set_state(AdminPanelStates.add_transaction)

@router.message(AdminPanelStates.add_transaction)
async def add_transaction_by_id(message: types.Message, state: FSMContext) -> None:
    """Add transaction by ID"""
    transaction_data = message.text.split(",")
    if len(transaction_data) != 3:
        await message.answer("Неверное количество аргументов")
        # show main menu
        await start(message)
        return
    transaction_data = {
        "user_id": transaction_data[0],
        "summ": transaction_data[1],
        "currency_id": 1,
        "type": transaction_data[2]
    }
    response = requests.post(base_url + "/api/api/transactions/create", headers=headers, json=transaction_data)
    if response.status_code == 201:
        await message.answer("Транзакция добавлена")
    else:
        await message.answer("Ошибка при добавлении транзакции")

    await state.clear()
    # show main menu
    await start(message)


@router.callback_query(TransactionCallback.filter(F.next_menu_prefix == "back"))
async def back_to_main_menu_transactions(query: types.CallbackQuery) -> None:
    """Back to main menu"""
    await start(query.message)