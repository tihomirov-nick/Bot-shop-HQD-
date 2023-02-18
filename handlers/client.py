from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from keyboards import button_case_client
from keyboards import button_case_client2
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from data_base import makeorder_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup



class FSMClient(StatesGroup):
	name = State()
	number_ = State()
	username = State()
	answer1 = State()
	contact = State()
	answer2 = State()

	


#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	await makeorder_db.sql_delete(message.from_user.id)
	await bot.send_message(message.from_user.id, "добро пожаловать", reply_markup=kb_client)
		

async def product_command(message : types.Message):
	await sqlite_db.sql_read(message)


#добавление первого товара в корзину
async def cm_buy(message : types.Message):
	read = await sqlite_db.sql_read2()
	for ret in read:
		await bot.send_message(message.from_user.id, f'--{ret[0]} {ret[1]}:\n   {ret[2]} шт [{ret[3]} р/шт]', reply_markup=InlineKeyboardMarkup().\
			add(InlineKeyboardButton(f'добавить в заказ {ret[0]}', callback_data=f'add {ret[0]}')))
	await FSMClient.name.set()

#отмена
async def cancel_handler(message : types.Message, state:FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('ok',reply_markup=kb_client)
	await makeorder_db.sql_delete(message.from_user.id)


async def add_name(callback_query: types.CallbackQuery, state:FSMContext):
	item = callback_query.data.replace('add ', '')
	name_list = await makeorder_db.sql_read_name(callback_query.from_user.id)
	try:
		lenght = 0
		for x in range(len(name_list)):
			if (item == name_list[x]):
				lenght+=1
				await callback_query.answer(text = 'вы уже добавили данный товар, выберите другой', show_alert=True)	
			
		if (lenght==0):
			async with state.proxy() as data:
				data['name'] = item
			await FSMClient.next()
			await callback_query.answer(text='укажите количество', show_alert=True)
	except ValueError:
		async with state.proxy() as data:
			data['name'] = item
		await FSMClient.next()
		await callback_query.answer(text='укажите количество', show_alert=True)


async def add_number_(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		number1 = int(await sqlite_db.sql_read_number_(data['name']))
		try:
			data['number_'] = int((message.text))
			if ((int(data['number_']) > int(number1)) or (int(data['number_'])<=0) ):
				await message.answer('в наличии нет такого количества, введите число меньше')
				return

			if (int(data['number_']) <= int(number1) and (int(data['number_'])>0)):
				await FSMClient.next()
				await message.answer('товар выбран', reply_markup=button_case_client2)
			

		except ValueError:
			await message.answer('введи число')

	
async def add_username(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['username'] = message.from_user.id
	await makeorder_db.sql_add_command(state)
	await message.answer('хотите добавить еще товар?', reply_markup=button_case_client)
	await FSMClient.next()


async def give_answer1(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['answer1'] = message.text

	if (data['answer1'] == 'да'):
		await message.answer('выбери товар', reply_markup=kb_client)
		await state.finish()
		await cm_buy(message)

	if (data['answer1'] == 'нет'):
		await message.answer('ведите контактные данные для связи с вами')
		await FSMClient.next()
		
		
		

async def contact(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['contact'] = message.text
		await message.answer('подтвердить заказ',reply_markup=button_case_client)
		await FSMClient.next()

async def give_answer2(message : types.Message, state:FSMContext):
	CHANNEL_ID = '-1001626199004'
	async with state.proxy() as data:
		data['answer2'] = message.text
	await state.finish()

	if (data['answer2'] == 'да'):
		await message.answer('заказ создан',reply_markup=kb_client)	
		contact = (str(data['contact']))
		name = await makeorder_db.sql_read_name(message.from_user.id)
		number = await makeorder_db.sql_read_number_(message.from_user.id)
		price = await sqlite_db.sql_read_price(name)
		total_price = []
		for x in range(len(number)):
			total_price.append(int(number[x])*int(price[x]))
		total_sum = sum(total_price)
		a =[contact, ' , '.join(name)+":", ' , '.join(number),'сумма заказа: '+str(total_sum)]
		await bot.send_message(CHANNEL_ID,'НОВЫЙ ЗАКАЗ')
		await bot.send_message(CHANNEL_ID, '\n '.join(a))
		await makeorder_db.sql_delete(data['username'])
		await sqlite_db.sql_change_number_(number, name)
		
	if (data['answer2'] == 'нет'):
		await message.answer('заказ отменен',reply_markup=kb_client)
		await makeorder_db.sql_delete(data['username'])


def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(cancel_handler, state="*", text = 'отмена')


	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(product_command, text='в наличии')
	dp.register_message_handler(product_command, commands=['stock'])
	dp.register_message_handler(cm_buy, commands=['buy'])

	dp.register_message_handler(cm_buy, text='купить')
	dp.register_callback_query_handler(add_name,  lambda x: x.data and x.data.startswith('add '), state=FSMClient.name)
	dp.register_message_handler(add_number_, state=FSMClient.number_)
	dp.register_message_handler(add_username, state=FSMClient.username)
	dp.register_message_handler(give_answer1, state=FSMClient.answer1)
	dp.register_message_handler(contact, state=FSMClient.contact)
	dp.register_message_handler(give_answer2, state=FSMClient.answer2)

	
	
	
		
