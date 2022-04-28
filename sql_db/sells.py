from .db_sql import Connect_db



class Sells_Manager:
	def __init__(self):
		self.conn = Connect_db()
		self.table = 'sells'

	def createSoldProduct(self, bellNum, username, proName, price, quantity, time):
		try:
			self.conn.create_(self.table, bell_num=bellNum, username=username, proName=proName, price=price, quantity=quantity, created_at=time)
			return True

		except Exception as e:
			raise e

	def update_product_(self, bellNum, username, proName, price, quantity):
		try:
			self.conn.update_(self.table,
			 bell_num=bellNum,
			  username=username, 
			  proName=proName, 
			  price=price, 
			  quantity=quantity)
			return True

		except Exception as e:
			raise e

	def delete_product_(self, rowId):
		rowId = f"bell_num='{rowId}'"
		try:
			self.conn.delete_(self.table, rowId)
			return True

		except Exception as e:
			return False

	def fetch_products_(self, condition):
		#if condition.isalpha():
			#cond = f'name={condition}'

		#if condition.isnumeric():
		cond = f"bell_num = {condition}"

		 
		return self.conn.fetch_All(self.table, cond)
		#return condition.isnumeric()

	def fetch_products_by_seller(self, username):
		cond = f"username='{username}'"
		return self.conn.fetch_All(self.table, cond)

		 
	def search_in_sells(self, **kwargs):
		try:
			data = self.conn.search_(self.table, kwargs) 
		
			return data
		except:
			return False

	def fetch_all_sells(self):
		try: 
			data = self.conn.fetch_(self.table) 
		
			return data
		except:
			return False


	def get_bell_num(self):
		rowName = 'bell_num'
		return self.conn.fecthRow(self.table, rowName)


	def fetchSellsByName(self, name):
		cond = f"productName='{name}'"
		return self.conn.fetch_All(self.table, cond)






if __name__ == '__main__':
	con = Sells_Manager()
	con.createProduct_('0001', 'hamza', 'isis', '1520', '1')

	print(con.get_bell_num()[0][0].split('=')[1])




