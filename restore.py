from sql_db.db_sql import Connect_db
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from restore_ import Ui_Dialog
from pay import Pay


class Restore:
	def __init__(self):

		self.con = Connect_db()
		self.ui = None

	def restore(self, this):
		

		Dialog = QtWidgets.QDialog()
		self.ui = Ui_Dialog()
		self.ui.setupUi(Dialog)
		Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
		Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
		self.ui.dtUser_r.hide()
		self.ui.dbt_r.stateChanged.connect(self.showDtUserInput)


		Dialog.show()
		res = Dialog.exec_()
		if res == QtWidgets.QDialog.Accepted:
			product_info = self.ui.proName_r.text()
			quantity = self.ui.Quantity_.text()
			username = self.ui.dtUser_r.text()
			if quantity.isdigit() == False:
				return QMessageBox.warning(this, 'Error', "ادخل الكمية على شكل ارقام فقط")
			self.restoredProducts(product_info , quantity, this.username, username)


	def showDtUserInput(self, int):
		if self.ui.dbt_r.isChecked():
			self.ui.dtUser_r.show()
		else:
			self.ui.dtUser_r.hide()


	def fetchAllRestoredProducts(self, this):
		table = this.ui.d_tableContent_2
		this.ui.stackedWidget.setCurrentWidget(this.ui.page_10)
		products = self.con.fetch_('resotred')
		table.setEnabled(False)

		if len(products) > 0:
			table.setRowCount(len(products))
			for row, i in enumerate( products):
				table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0]))) #id
				table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))#name
				table.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2])) #seller
				table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3]))) #created_at

			table.sortItems(3, QtCore.Qt.DescendingOrder)


	def restoredProducts(self, inputData, qun, seller, username):
		BARCODE = 11
		created_at = datetime.datetime.today()

		if inputData.isalnum() == False:
			return False

		if inputData.isdigit() and len(inputData) >= BARCODE:
			#the input is barcode
			condition = f'ref="{inputData}"'

		elif inputData.isdigit() and len(inputData) < BARCODE:
			#the input is just a price
			if username:
				Pay().create_or_update(username=username, amount=inputData)
				

			return self.con.create_('resotred', name=inputData, seller=seller, created_at=created_at )

		elif inputData.isalpha():
			condition = f'name="{inputData}"'

		product = self.con.fetch_All('products', condition)[0]
		quantity = product[4]
		quantity = float(quantity) + float(qun)
		self.con.update_('products', condition, quantity=quantity)
		self.con.create_('resotred', name=product[2], seller=seller, created_at=created_at )
		#update debt payment table

		if username:
			Pay().create_or_update(username=username, amount=product[3])
			

		return True
		


if __name__ == '__main__':
	con = Restore()

	print(con.restoredProducts('12345678912', 'hamza', 'ali'))


