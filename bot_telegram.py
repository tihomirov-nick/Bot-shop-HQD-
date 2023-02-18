from aiogram.utils import executor 
from create_bot import dp
from data_base import sqlite_db
from data_base import makeorder_db
from aiogram import types

async def on_startup(dp):
	print('bot online')

	sqlite_db.sql_start()
	makeorder_db.sql_start()

	await dp.bot.set_my_commands([
        types.BotCommand("start", "запустить бота"),   
        types.BotCommand("stock", "посмотреть наличие товара"), 
        types.BotCommand("buy", "купить товар"), 
        
    ])

from handlers import admin, client, other 

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)