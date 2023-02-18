import sqlite3 as sq 
from create_bot import bot

def sql_start():
	global base, cur
	base = sq.connect('makeorder.db')
	cur = base.cursor()
	if base:
		print("data base 'makeorder.db' connected")
	base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT , number_ TEXT, username TEXT)')
	base.commit()


async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO menu VALUES (?, ?, ?)', tuple(data.values()))
		base.commit() 


async def sql_read_name(message):
	name = []
	for ret in cur.execute('SELECT name FROM menu WHERE username = ?', (message,)).fetchall():
		name.append(f'{ret[0]}')
	return(list(name))
	


async def sql_read_number_(message):
	number_ = []
	for ret in cur.execute('SELECT number_ FROM menu WHERE username = ?', (message,)).fetchall():
		number_.append(f'{ret[0]}')
	return(list(number_))


	
	



async def sql_delete(data):
	cur.execute('DELETE FROM menu WHERE username = ?', (data,))
	base.commit() 
	