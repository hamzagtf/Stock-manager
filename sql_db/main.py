from .db_sql import Connect_db



class Product_manager:
	def __init__(self):
		self.conn = Connect_db()
		self.table = 'products'
 
	def createProduct(self, ref, name, price, quantity, price_buy, proType, expire, created_at):
		try:
			self.conn.create_(self.table, 
			ref=ref, name=name, 
			price=price, 
			quantity=quantity, 
			price_buy=price_buy,
			type=proType, expire=expire, expired="false", created_at=created_at)
			return True

		except Exception as e:
			raise e

	def update_product(self, con,  name, price, quantity):
		con = f'rowid = "{con}"'
		try:
			self.conn.update_(self.table, con, name=name, price=price, quantity=quantity)
			return True

		except Exception as e:
			return  False

	def delete_product(self, ref):
		try:
			self.conn.delete_(self.table, f'rowid="{ref}"')
			return True

		except Exception:
			return False

	def fetch_products(self, condition):
		return self.conn.fetch_All(self.table, condition)
		


	def search_in_products(self, **kwargs):
		try:
			data = self.conn.search_(self.table, kwargs) 
		
			return data
		except:
			return False

	def fetch_all_products(self):
		try:
			data = self.conn.fetch_(self.table) 
		
			return data
		except Exception as e:
			raise e


	def get_pro_id(self):
		rowName = 'ROWID'
		return self.conn.fecthRow(self.table, rowName)





if __name__ == '__main__':
	con = Product_manager()
	#createProduct(self, ref, name, price, quantity, price_buy, proType, expire, created_at)
	con.createProduct('1', 'v', '15', '15', "15", "None", "15/10/2020", "15/10/2010")
	
	#con.delete_product("1520")
	#print(con.fetch_products('h'))




