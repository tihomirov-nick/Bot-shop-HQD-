from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
	name = State()
	description = State()
	number_ = State()
	price = State()


#для изменения количества
class FSMAdmin2(StatesGroup):
	message_text1 = State()
	number1_ = State()
	

#@dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message: types.Message):
	global ID 
	ID = message.from_user.id 
	await message.delete()
	await bot.send_message(message.from_user.id, 'Доступ разрешен', reply_markup=admin_kb.button_case_admin)
	

#начало диалога
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
	if message.from_user.id == ID:
		await FSMAdmin.name.set()
		await message.reply('Введи название и вкус')


#меняем кол-во по названию
async def cm_change(message : types.Message):
	if message.from_user.id == ID:
		read = await sqlite_db.sql_read2()
		for ret in read:
			await bot.send_message(message.from_user.id,  f'--{ret[0]} {ret[1]}:\n   {ret[2]} шт [{ret[3]} р/шт]', reply_markup=InlineKeyboardMarkup().\
				add(InlineKeyboardButton(f'изменить количество {ret[0]}', callback_data=f'change {ret[0]}')))
		await FSMAdmin2.message_text1.set()


#выход из состояния
#@dp.message_handler(state="*", commands = 'Отмена')
#@dp.message_handler(Text(equals='Отмена',ignore_case=True),state="*")
async def cancel_handler(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('ok')


#ловим ответ
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_name(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply('Введи описание')
		

#ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_description(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['description'] = message.text
		await FSMAdmin.next()
		await message.reply('Введи количество')


#ловим третий ответ
#@dp.message_handler(state=FSMAdmin.description)
async def load_number_(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['number_'] = message.text
		await FSMAdmin.next()
		await message.reply('Укажи цену')


#ловим последний ответ
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['price'] = message.text
		await sqlite_db.sql_add_command(state)
		await state.finish()
		await message.reply('Успешно')


#посмотреть меню
async def show_product(message : types.Message):
	if message.from_user.id == ID:
		await sqlite_db.sql_read(message)


#изменить количество
async def change_item(callback_query: types.CallbackQuery,state:FSMContext):
	item = callback_query.data.replace('change ', '')
	async with state.proxy() as data:
		data['message_text1'] = item
	await FSMAdmin2.next()
	await callback_query.answer(text='введи количество', show_alert=True)
	

async def change_item2(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['number1_'] = message.text
		await sqlite_db.sql_change(state)
		await state.finish()
		await message.reply('Успешно')


#удалить 
#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def delete_item(callback_query: types.CallbackQuery):
	await sqlite_db.sql_delete(callback_query.data.replace('del ', ''))
	await callback_query.answer(text='успешно', show_alert=True)


async def delete_item1(message: types.Message):
	if message.from_user.id == ID:
		read = await sqlite_db.sql_read2()
		for ret in read:
			await bot.send_message(message.from_user.id,  f'--{ret[0]} {ret[1]}:\n   {ret[2]} шт [{ret[3]} р/шт]', reply_markup=InlineKeyboardMarkup().\
				add(InlineKeyboardButton(f'удалить {ret[0]}', callback_data=f'del {ret[0]}')))
		

def register_handlers_admin(dp : Dispatcher):
	dp.register_message_handler(cm_start, text='загрузить', state=None)
	dp.register_message_handler(cancel_handler, state="*", text = 'отмена')
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_description, state=FSMAdmin.description)
	dp.register_message_handler(load_number_, state=FSMAdmin.number_)
	dp.register_message_handler(load_price, state=FSMAdmin.price)
	dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
	dp.register_message_handler(show_product, text='в наличии')
	dp.register_message_handler(cm_change, text='изменить количество', state=None)
	dp.register_callback_query_handler(change_item,  lambda x: x.data and x.data.startswith('change '), state=FSMAdmin2.message_text1)
	dp.register_message_handler(change_item2, state=FSMAdmin2.number1_)
	dp.register_callback_query_handler(delete_item, lambda x: x.data and x.data.startswith('del '))
	dp.register_message_handler(delete_item1, text='удалить')
	
	
	
	
	
	



