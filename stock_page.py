from multiprocessing import Condition
from sql_db import main
from sql_db import debet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from add_product import Ui_Dialog as AddProduct
import datetime

class Stock:

	def __init__(self):
		self.ui = main.Product_manager()



	
	def add_new_product(self, table, lcd, this, ):

		Dialog = QtWidgets.QDialog()
		ui = AddProduct()
		ui.setupUi(Dialog)
		Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
		Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

		Dialog.show()
		res = Dialog.exec_() 
					
		if res == QtWidgets.QDialog.Accepted:
			
			ref = ui.s_barcode.text().strip()
			name = ui.s_proName.text().strip()
			price = ui.s_price.value()
			price_buy = ui.s_price_2.value()
			quantity = ui.s_quantity.value()
			protype = 'None'
			expire_date = ui.dateEdit.date().toPyDate()
			dates = datetime.datetime.now().strftime("%c")
			#check if product has a code bar 
			
			
			if len(name) == 0 or price == 0 or quantity == 0:
				QMessageBox.warning(this, 'Error', 'المجالات فارغة')
			
			elif self.checkProductEx(name, ref):
				QMessageBox.warning(this, 'Error', 'هذا المنتج موجود قم بتحديثه فقط')

			elif ui.checkBox.isChecked() == True and len(ref) == 0:
				#create product without barcode
				self.ui.createProduct('None', name, price, quantity, price_buy, 'l', expire_date, dates)
				QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
			else:		
				self.ui.createProduct(ref, name, price, quantity, price_buy, 'None', expire_date, dates)
				QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
			
			self.fetchAllProducts(table, lcd)

			
			

	def search_in_products(self, keyword, table, lcd):
		keywords = keyword.text().strip()
		keyWordResult = self.ui.search_in_products(name=keywords, ref=keywords)
		row = 0
		if len(keyWordResult) != 0:
			table.setRowCount(len(keyWordResult))
			for i in keyWordResult:
				
				table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))#id
				table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))#name
				table.setItem(row, 2, QtWidgets.QTableWidgetItem(i[4]))#quantity
				table.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))#buy
				table.setItem(row, 4, QtWidgets.QTableWidgetItem(i[5]))#sell
				table.setItem(row, 5, QtWidgets.QTableWidgetItem(i[7]))#expired
				table.setItem(row, 6, QtWidgets.QTableWidgetItem(i[9]))#created at
				row = row +1 


			lcd.display(float(len(keyWordResult)))


	def fetchAllProducts(self, table, lcd):
		info = self.ui.fetch_all_products()
		row = 0
		table.setRowCount(len(info))
		for i in info:
			
			table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))#id
			table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))#name
			table.setItem(row, 2, QtWidgets.QTableWidgetItem(i[4]))#quantity
			table.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))#buy
			table.setItem(row, 4, QtWidgets.QTableWidgetItem(i[5]))#sell
			table.setItem(row, 5, QtWidgets.QTableWidgetItem(i[7]))#expired
			table.setItem(row, 6, QtWidgets.QTableWidgetItem(i[9]))#created at

			row = row +1

		self.setProducNumber(table, lcd)

	def checkProductEx(self, proName, ref):
		condition = f'name="{proName}" OR ref="{ref}"'
		product = True if len(self.ui.fetch_products(condition)) > 0 else False
		return product

	def setProducNumber(self, table, lcd):
		
		num = table.rowCount()
		lcd.display(float(num))


	def removeProduct(self,this, table, lcd):
		
		
		row = table.currentRow()
		if row >= 0:
			x = lcd.value() -  float(1)
			lcd.display(x)
			
			p_id = table.item(row, 0).text()
			self.ui.delete_product(p_id)
			table.removeRow(row)
			QMessageBox.information(this, 'Info', "تمت العملية بنجاح")
			

	def updateProducts(self, this, table):
		try:
			row = table.currentRow()
			
			
			rowid = table.item(row, 0).text().strip()
			name = table.item(row, 1).text().strip()
			price = table.item(row, 3).text().strip()
			quantity = table.item(row, 2).text().strip()
			if len(name) != 0 and len(price) != 0 and len(quantity) != 0:

				if self.ui.update_product(rowid,name, price, quantity):
					QMessageBox.information(this, 'Info', "تمت العملية بنجاح")

				else:
					self.errorMsg(this)
			else:
				self.errorMsg(this)
		except AttributeError:
			pass


	def errorMsg(self, this):
		QMessageBox.warning(this, "Error", "حدث خطأ")
				






if __name__ == "__main__":
	d =Stock()
	print(d.checkProductEx('hamza'))
			
