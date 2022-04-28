from sql_db.main import Product_manager
from sql_db.sells import Sells_Manager
from sql_db.db_sql import Connect_db
import datetime

class Analytics:
	def __init__(self):
		self.products = Product_manager()
		self.sells = Sells_Manager()
		self.con = Connect_db()


	def fetchProductPrices(self, name):
		condition = f'name="{name}"'
		products = self.products.fetch_products(condition)
		prices = (float(products[0][3]), float(products[0][5]), float(products[0][4]))
		return prices # sell price and buy price and quantity

	def fetchSoldProductsQuantity(self, name):
		""" return a float of quantity for 
		products with that name """

		sold_products = self.sells.fetchSellsByName(name)
		soldProductQuantity = float(0)
		for quantity in sold_products:
			soldProductQuantity += float(quantity[5])

		return soldProductQuantity 

	def totalProductEarn(self, name):
		""" count the total earns of each product """
		sellPrice, buyPrice, quantity = self.fetchProductPrices(name)
		if quantity == 0:
			return False

		differnce = buyPrice - sellPrice
		result = differnce * quantity

		return result

	def totalSoldProductsEarn(self, name):
		sellPrice, buyPrice, _= self.fetchProductPrices(name)
		quantity = self.fetchSoldProductsQuantity(name)

		differnce = buyPrice - sellPrice
		result = differnce * quantity

		return result

	def mostSoldProducts(self):
		products = self.sells.fetch_all_sells()
		products_quantity = []
		products_name = set()

		for product in products:
			product_name = product[3]
			_products_name = True if product_name != None and product_name not in products_name and products_name != '/' else False

			if _products_name and product_name != '/':


				product_quantity = self.fetchSoldProductsQuantity(product_name)
				products_quantity.append({
					product_name : product_quantity
					})
				products_name.add(product_name)

		#products_quantity.sort(reverse=True)

		return products_quantity[:20]

	def totalEarns(self):
		products = self.products.fetch_all_products()
		if products:
			total = float(0)
			for i in products:
				name = i[2]
				total += float(self.totalProductEarn(name))


			return total

		return 

	def allSoldProductsLength(self):
		result = len(self.sells.fetch_all_sells())
		return result

	def get_date(self, date):
		sold_products =self.con.fetch_All('sells', f'created_at="{date}"')
		if sold_products:
			dates = sold_products[0][6]
			
			date = dates.split('-')
			year = date[0]
			month = date[1]
			day = date[2][:2].strip()
			
			return (day, month, year)

		return 
				

	def earnPerDay(self, date):
		
		#date = str(datetime.datetime.today().date())
		data = self.con.fetch_All('sells', f'created_at="{date}"')
		result = float(0)
		if date:
			for i in data:
				product_name = i[3]
				quantity = i[5]

				if product_name != '/':
					sell_product_prices, buy_product_prices, _ = self.fetchProductPrices(product_name)
					product_earns = buy_product_prices - sell_product_prices
					result += float(product_earns) * float(quantity)

				else:
					result += float(i[4])

			return result


	def sevenDaysDates(self):
		today_date = datetime.datetime.today().date()
		today_day = f'0{today_date.day}' if today_date.day <= 9 else today_date.day
		today_month = f'0{today_date.month}' if today_date.month <= 9 else today_date.month
		today_year = today_date.year
		dates = []
		for i in range(today_day - 6, today_day + 1):
			date = (today_year,today_month, i)
			dates.append(date)

		return dates


	def daysOfTheWeek(self):
		dates = self.sevenDaysDates()
		days = []
		for date_ in dates:
			date = datetime.datetime(date_[0], int(date_[1]), int(date_[2])).strftime('%A')
			days.append(date)

		return days

	def sevenDaysEarns(self):
		dates = self.sevenDaysDates()
		earns_a_day = []
		for date in dates:
			date_ = f'{date[0]}-{date[1]}-{date[2]}'
			earns_a_day.append(self.earnPerDay(date_))

		return earns_a_day






		


				




				
		
	


		


if __name__ == '__main__':
	con = Analytics()
	print(con.sevenDaysEarns())