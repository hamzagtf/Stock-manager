import sqlite3 

import json

class Connect_db:
	#create table

	# create functions that handle sql

	def __init__(self):
		self.conn = sqlite3
		self.db = self.conn.connect('test.db', check_same_thread=False)
		self.con = self.db.cursor()
		self.con.execute("""CREATE TABLE IF NOT EXISTS admin(
			username text  ,
			password text,
			phone text  ,
			role text  ,
			dbt text ,
			settings text,
			stock text,
			created_at date )""")

		self.con.execute("""CREATE TABLE IF NOT EXISTS resotred(
			name text  ,
			seller text,
			created_at date )""")

		self.con.execute("""CREATE TABLE IF NOT EXISTS pay(
			username text  ,
			pay text,
			created_at date )""")

		self.con.execute("""CREATE TABLE IF NOT EXISTS products(
			ref text  ,name text  ,
			price text  ,quantity text  , price_buy text,
			expire text  ,type text, expired int, created_at date )""")

		self.con.execute("""CREATE TABLE IF NOT EXISTS debet_users_accounts(
			username text,
			phoneNum text,
			created_at date)""")


		self.con.execute("""CREATE TABLE IF NOT EXISTS debet_users(
			bellNum text,username text,
			productName text,price text,
			quantity text,created_at date)""")

		#self.create_('debet_users_accounts', username="hamza", phoneNum="077565482", created_at="10-10-2020")


		self.con.execute("""CREATE TABLE  IF NOT EXISTS sells(
			bell_num text,username text,
			productName text,price text,
			quantity text,created_at date)""")
		
		
		#with open('D:/ecommerce_project/project/Ecommerce/sql_db/db.json') as f:
			#posts = json.load(f)

		#for post in posts:
			#self.create_('products',

			#ref=post['ref'],
			#name=post['name'],
			#price=post['price'],
			#quantity=post['quantity'],
			#expire=post['expire'],
			#created_at=post['created_at'])
	




	def create_(self, table, **kwargs):
		data = []

		for index, value in kwargs.items():
			data.append(f':{index}')

		
		data = ', '.join(data)
		data = f'({data})'
		with self.db:
			self.con.execute(f"""
				INSERT INTO {table} VALUES {data}
				""", kwargs)
		return 'done'
		
		


	def update_(self, table,con, **kwargs):
		data = []

		for index, value in kwargs.items():
			
			if value != None:
				data.append(f'{index} = "{value}"')

		data = ', '.join(data)
		with self.db:
			self.con.execute(f"""
				UPDATE {table} SET {data} WHERE {con}
				""")
		
		return 'done'

	def delete_(self, table, rowId):
		with self.db:
			self.con.execute(f"""
				DELETE FROM {table}  WHERE {rowId}
				""")
		return 'done'


	def fetch_All(self, table, data):
		#data = []
		#for index, value in kwargs.items():
			#data.append(f"{index} = '{value}'")
		#data = ' AND '.join(data)

		#print(data)

		with self.db:
			self.con.execute(f"""
				SELECT rowid, * FROM {table} WHERE { data }""",)
		return self.con.fetchall()


	def search_(self, table, kwargs):
		data = [] 
		for index, value in kwargs.items():
			data.append(f'{index} LIKE "%{value}%"')

		data = ' OR '.join(data)
		return self.fetch_All(table, data)
	

	def fecthRow(self, table, rowName, con):
		with self.db:
			self.con.execute(f"""
				SELECT {rowName} FROM {table} WHERE {con} """)
		return self.con.fetchall()


	def fetch_(self, table):
		with self.db:
			self.con.execute(f"""
				SELECT rowid, * FROM {table}""")
		return self.con.fetchall()


	


if __name__ == '__main__':
	db = Connect_db()
	#db.create_('products',ref='150', name='data', price='150', quantity="150",expire ='125', created_at= '150')
	#x = db.create_('products',ref='150', name='isis', price='150', quantity="150", created_at='125', expire='150')
	#db.delete_('products', 'ref="5000"')
	print(db.fetch_('products'))
	#print(x)

