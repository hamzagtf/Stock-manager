from home import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from home_page import Home_page as hp
from stock_page import Stock
from debet_page import DebetPage
from seller import Sells
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.Qt import Qt
from admin.index import Admin
from barcodeGenerater.index import Barcode
from import_and_export.exportDB import ExportDB
from import_and_export.update_products_db import Update_DB
from import_and_export.importDB import ImportDB
from expired import Expired
from restore import Restore
from analytics.index import AnalyticsView
from keyEvent import key_Events


class Main_Window(QMainWindow):
	def __init__(self):

		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.admin = Admin()

		#login access

		role = ""
		self.username = None
		self.role = None
	
		#page navigator btns 
		self.ui.HOME.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page))
		self.ui.STOCK.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
		
		self.ui.SELLS.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
		self.ui.DEBT.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
		self.ui.EXIT.clicked.connect(
			lambda:self.exit())
		self.ui.sideBar.hide()
		
		self.ui.signin.clicked.connect(
			lambda:self.signIn(self))
		#hide password

		self.ui.password.setEchoMode(QLineEdit.Password)

		
		
		
		#home page component 
		self.ui.sell.clicked.connect(lambda:self.hp.sellPro(self,
			self.username,
			self.ui.h_table, 
			self.ui.h_lcd,
			self.ui.h_bell_num))

		self.ui.h_add.clicked.connect(lambda:self.hp.insert_to_table(
			self.ui.h_table, 
			self.ui.h_input,
			self.ui.h_lcd))

		self.ui.h_delete.clicked.connect(lambda:self.hp.remove_row(
			self.ui.h_table, 
			self.ui.h_lcd))
		

		self.ui.addToDebt.clicked.connect(lambda:self.hp.debt_user_name(self,
			self.ui.h_table, 
			self.ui.h_lcd,
			self.ui.h_bell_num,
			self.ui.h_bell_num))

		self.ui.h_input.textChanged.connect(lambda:self.hp.readBarCode(
			self.ui.h_table,
			self.ui.h_input, 
			self.ui.h_lcd ))

		self.ui.printBell.clicked.connect(lambda:self.hp.show_bell_doc(self.ui.h_table))

		
		self.hp =  hp()
		self.ui.h_bell_num.setText(str(f'0000{self.hp.bellNum()}'))

		#restore product
		self.ui.restore.clicked.connect(lambda:Restore().restore(self))
		self.ui.restore_page.clicked.connect(lambda:Restore().fetchAllRestoredProducts(self))


		#stock page component

		self.sp = Stock()
		self.ui.s_add.clicked.connect(
			lambda: self.sp.add_new_product(self.ui.s_table,self.ui.s_lcd, self))
		
		self.ui.STOCK.clicked.connect(
			lambda:self.sp.fetchAllProducts(self.ui.s_table, self.ui.s_lcd))
		
		self.ui.s_input.textChanged.connect(
			lambda:self.sp.search_in_products(
				self.ui.s_input, 
				self.ui.s_table,
				self.ui.s_lcd))
		#self.sp.setProducNumber(self.ui.s_table, self.ui.s_lcd)
		self.ui.s_delete.clicked.connect(lambda:self.sp.removeProduct(self,
			self.ui.s_table, self.ui.s_lcd))

		self.ui.s_update.clicked.connect(
			lambda:self.sp.updateProducts(self, self.ui.s_table))


		#sells page component --------------------------
		self.sl = Sells()
		self.ui.SELLS.clicked.connect(lambda:self.sl.fetchAllSells(
			self.ui.bellTable,
			self.username,
			self.role))
		
		self.ui.bell_input.textChanged.connect(
			lambda:self.sl.search_in_sells(
				self.ui.bell_input, 
				self.ui.bellTable,
				self.username,
				self.role))

		self.ui.deleteBell.clicked.connect(lambda:self.sl.removeProduct(self,
			self.ui.bellTable))
		self.ui.showBell.clicked.connect(lambda:self.sl.showBell(self.ui.bellTable))



		#debet page component--------------------------------
		self.db = DebetPage()

		self.ui.DEBT.clicked.connect(
			lambda:self.db.fetch_All_Users(self, self.ui.d_tableContent))
		
		self.ui.d_search_input.textChanged.connect(
			lambda:self.db.search_In_Users(self.ui.d_search_input, self.ui.d_tableContent))
		

		self.ui.d_deleteUser.clicked.connect(
			lambda:self.db.removeUser(
				self,self.ui.d_tableContent,
				self.ui.d_total ))

		self.ui.d_addUser.clicked.connect(
			lambda:self.db.add_new_dt_user(self))

		self.ui.d_showBook.clicked.connect(
			lambda:self.db.showBook(
				self.ui.stackedWidget, 
				self.ui.page_5,
				self.ui.d_tableContent,
				self.ui.u_page_table,
				self.ui.u_page_name,
				self.ui.u_page_phone,
				self.ui.label_6))
		self.ui.updateInfo.clicked.connect(
			lambda:self.db.updateUserDtInfo(self,
			self.ui.label_6,
			self.ui.u_page_name,
			self.ui.u_page_phone,))

		self.ui.u_page_delete.clicked.connect(
			lambda:self.db.removeUserBell(self,self.ui.u_page_table))
		self.ui.u_page_show.clicked.connect(
			lambda:self.db.showUserDbtBell(self.ui.u_page_table))
		self.ui.pay.clicked.connect(
			lambda:self.db.pay(self))


	    #settings page
		self.ui.SETTINGS.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page_8))
		
		self.ui.user_settings.clicked.connect(
			lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.page_7))
		self.ui.gen_barcode.clicked.connect(
			lambda:Barcode().generate_Bar_Code())
		self.ui.exDB.clicked.connect(
			lambda:ExportDB().export())

		self.ui.download.clicked.connect(lambda:ImportDB(self).openFile())
		self.ui.saveTodb.clicked.connect(lambda:ImportDB(self).spinner())

		#admin pge 

		table = self.ui.table_user

		self.admin.fetch_ALL_Users(table)
		self.ui.add_user.clicked.connect(lambda:self.admin.create_seller(self, self.ui.table_user))
		self.ui.update_user.clicked.connect(lambda:self.admin.update_seller(self))
		self.ui.delete_user.clicked.connect(lambda:self.admin.delete_seller(self, self.ui.table_user))

		#expired page

		Expired().expired_products(self)
		self.ui.expired_date.clicked.connect(lambda:Expired().fetchExpiredProducts(self))
		#analytics

		self.ui.analytic.clicked.connect(lambda:AnalyticsView(self))
		#AnalyticsView(self)


	def exit(self):
		self.ui.sideBar.hide()
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)
	
	def signIn(self, this):
		log_in = Admin().check_user_login(this, self.ui)

		if log_in != None:
			self.username, password, self.role = log_in

	def keyPressEvent(self, e):
		
		key_Events(self, e)
		



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Main_Window()
    ui.show()
    
    sys.exit(app.exec_())