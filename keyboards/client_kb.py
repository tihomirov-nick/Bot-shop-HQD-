from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



b1 = KeyboardButton('в наличии')
b2 = KeyboardButton('купить')
b3 = KeyboardButton('отмена')




kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

kb_client.row(b1,b2)
kb_client.add(b3)


b4 = KeyboardButton('да')
b5 = KeyboardButton('нет')

button_case_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_case_client.row(b4,b5)

b6 = KeyboardButton('продолжить')

button_case_client2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_case_client2.row(b6)