from sql_db.db_sql import Connect_db
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import datetime


class Expired:

	def __init__(self):

		self.con = Connect_db()
		self.table = 'products'


	def _expired_products(self):
		todayDate =datetime.date.today()
		products = self.con.fetch_(self.table)
		expired = 0
		products_id = []
		if products:
			for pro in products:
				product = pro[7].split('-')
				
				product = datetime.date(2023, 3, 17)
				expiredDate = product - todayDate

				if expiredDate.days <= 20:
					
					self.con.update_(self.table, f"rowid='{pro[0]}'", expired="true")
					expired += 1 

				elif float(pro[4]) <= float(15):
					expired += 1

				
		return (expired, products_id)


	def expired_products(self, this):
		products = self._expired_products()
		expiredProductNumber = products[0] if products else 0
		print(expiredProductNumber )
		if expiredProductNumber > 0:
			this.ui.ex_number.show()
			return this.ui.ex_number.setText(f"  {str(expiredProductNumber)}")

		this.ui.ex_number.setText('0')
		return this.ui.ex_number.hide()


	


	def fetchExpiredProducts(self, this):
		
		LIMIT_QUANTITY = float(13)
		DANGER_QUANTITY = float(15)

		condition = "expired='true' OR quantity<=15"
		products = self.con.fetch_All(self.table, condition)
		table = this.ui.expired_table
		this.ui.stackedWidget.setCurrentWidget(this.ui.page_9) #set page
		this.ui.ex_number.hide() #remove notification


		table.setRowCount(len(products))
		table.setEnabled(False)


		for row, i in enumerate(products):
			#fill the table with info 
			barcode = i[1]
			name = i[2]
			quantity = float(i[4])
			dateExpired = i[7]
			_dateExpired = i[8]

			table.setItem(row, 0, QtWidgets.QTableWidgetItem(barcode)) #barcode
			table.setItem(row, 1, QtWidgets.QTableWidgetItem(name)) #name
			table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(quantity))) #quantity
			table.setItem(row, 3, QtWidgets.QTableWidgetItem(dateExpired)) #date Expired
			
			#add color to specific rows

			if quantity <= LIMIT_QUANTITY :
				table.item(row, 2).setBackground(QtGui.QColor('red'))#quantity

			elif quantity <= DANGER_QUANTITY:
				table.item(row, 2).setBackground(QtGui.QColor('orange'))#quantity


			if  _dateExpired == 'true':
				table.item(row, 3).setBackground(QtGui.QColor('red'))#date expired

			 
			


				

			