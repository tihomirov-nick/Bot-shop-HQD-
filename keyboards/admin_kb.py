from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import sqlite_db



button_load = KeyboardButton("загрузить")
button_delete = KeyboardButton("удалить")
button_change = KeyboardButton("изменить количество")
button_cancel = KeyboardButton("отмена")
button_menu = KeyboardButton("в наличии")



button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_case_admin.row(button_load, button_delete, button_change)
button_case_admin.row(button_cancel, button_menu)


