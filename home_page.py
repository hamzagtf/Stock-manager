from sql_db import main, debet, sells
from audioplayer import AudioPlayer
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from d_user import Ui_Dialog 
from quantity import Ui_Dialog as Quantity
import datetime
from printDoc import PrintDoc
from expired import Expired
import re

class Home_page:

	def __init__(self):
		self.Pmanage = main.Product_manager()
		self.dt = debet.DebetManager()	
		self.sl = sells.Sells_Manager()
		
		
	def debt_user_name(self,this, table, lcd,txt, bNum):
		""" this is the dialog box that fetch 
		the dbt username  """


		if table.rowCount() != 0:
			Dialog = QtWidgets.QDialog()
			ui = Ui_Dialog()
			ui.setupUi(Dialog)
			Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
			Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

			#self.get_debt_usr(ui.debt_username, self.dt.fetchNames(ui.debt_username.text().strip()))
			Dialog.show()
			res = Dialog.exec_()
			if res == QtWidgets.QDialog.Accepted:

				name = ui.debt_username.text().strip()

				if len(name) != 0:
					if len(self.dt.fetch_Debt_User(name)) > 0:
						self.add_to_debt(this, table, name, lcd,txt, bNum.text())
						QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
					else:
						QMessageBox.warning(this, 'Error', 'هذا الاسم غير موجود')
				
			else:
				return 
		


	def check_input(self, text):
		""" return a list of data from db
		after filtering it """
		res = text != '' and all(chr.isalpha() or chr.isspace() for chr in text)
		if res:
			#need editing
			result = self.Pmanage.fetch_products(f'name="{text}"')
			if len(result ) > 0:
				result = self.Pmanage.fetch_products(f'name="{text}"')[0]
			else:
				result = False
			return result

		elif text.isdigit(): #it is price
			if len(text) < 9:
				return ['/', '/', '/', text]
			else:
				#need editing
				result = self.Pmanage.fetch_products(f'ref="{text}"')
				if len(result) == 0:
					result = False
				else:
					result = self.Pmanage.fetch_products(f'ref="{text}"')[0]
				return result

	def insert_to_table(self,table, t_input,lcd):
		""" insert info to table after checking it
		from db """
		
		t = t_input.text().strip()
		res = t!= '' and all(chr.isalpha() or chr.isspace() for chr in t)
		
		if len(t) != 0 and t.isalnum() or res:
			inputText = self.check_input(t)
			
		else:
			inputText = False
			
		if inputText != False:
			#inserting data into table
			quantity = 1
			if type(inputText) == tuple:
				productType = inputText[6]
				barcode = inputText[1]
				
				if barcode == 'None':
					quantity = self.enterQuantity()
					productType = True
			else:
				productType = False

			row = table.rowCount()
			x = False
			if row > 0:
				for i in range(row):
					if table.item(i, 0).text() == str(inputText[0]) and str(inputText[0]) != "/":
						x = True
						rows = i		
			if x:
				if quantity != None and inputText[3].isdigit():
					prices = float(inputText[3]) * float(quantity) if productType else float(inputText[3])
					quantity = float(table.item(rows, 2).text()) + float(quantity)
					price = float(table.item(rows, 3).text()) + prices
					table.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(price)))
					table.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(quantity)))
					p = lcd.value() + float(prices)
					lcd.display(p)
					
			else:
				if quantity != None and inputText[3].isdigit():
					price = float(inputText[3]) * float(quantity) if productType else float(inputText[3])
				
					table.setRowCount(row + 1)
					table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(inputText[0])))
					table.setItem(row, 1, QtWidgets.QTableWidgetItem(inputText[2]))
					table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(quantity)))
					table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(price)))
					p = lcd.value() + price
					lcd.display(p)

			t_input.setText('')
			



	def enterQuantity(self):
		Dialog = QtWidgets.QDialog()
		ui = Quantity()
		ui.setupUi(Dialog)
		Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
		Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

		Dialog.show()
		res = Dialog.exec_()
		if res == QtWidgets.QDialog.Accepted:
			return ui.lineEdit.text()		

	def readBarCode(self, table, barcode, lcd):
		b = barcode.text().strip()
		if len(b) >= 13 and b.isdigit():
			self.insert_to_table(table, barcode, lcd) 


	def remove_row(self, table, lcd):
		""" removing row info from table """
		
		if table.rowCount() > 0:
			row = table.currentRow()
			if row >= 0:
				val = table.item(row, 3).text()
				x = lcd.value() -  float(val)
				lcd.display(x)
				table.removeRow(row)

	def fetch_table_info(self, table):
		""" this function return all the table
		info as lists inside list i.e each row 
		will be inside a list   """

		row = table.rowCount()
		result = []
		
		for r in range(row): 
			data = []
			result.append(data)
			for j in range(4):
				data.append(table.item(r, j).text())

		return result

	def sellPro(self,this, username, table, lcd, txt):
		""" In here we insert table info i.e sold
		products into db  """

		b_num = int(txt.text()) + 1
		seller =  username
		if table.rowCount() != 0:
			try: 
				
				info = self.fetch_table_info(table)
				x = datetime.datetime.today().date()
				for i in info:
					self.sl.createSoldProduct(b_num, seller, i[1],i[3], i[2],x)
					self.updateProductQuantity(this, i[0], i[2])
					table.setRowCount(0)
					lcd.display(0)

				
			
				txt.setText(f'0000{str(b_num)}')
			except Exception as e:
				raise e

	def add_to_debt(self,this, table, username, lcd, txt, bNum):
		""" this function handel the debet users 
		after it also insert data to sell db

		"""
		seller = this.username
	
		b_num = int(txt.text()) + 1
		date = datetime.datetime.today().date()

		try:
			info = self.fetch_table_info(table)
			for i in info:
				#insert data into dbet users db
				self.dt.createUser(bNum, username, i[1], i[3], i[2], date)
				self.updateProductQuantity(this, i[0], i[2])

				

				#insert bell into sold products
				self.sl.createSoldProduct(b_num, seller,  i[1], i[3], i[2], date)
				table.setRowCount(0)
				lcd.display(0)
			txt.setText(f'0000{str(b_num)}')

		except Exception as e:
			raise e

	def updateProductQuantity(self, this, proId, quan):
		try:
			product = self.Pmanage.fetch_products(f'rowid="{proId}"')[0]
			quantity = float(product[4])
			name = product[2]
			price = product[3]
			
			if quantity > 0: 
				quantity = quantity - float(quan)
				self.Pmanage.update_product(proId,  name, price, str(quantity))
			else:
				QMessageBox.warning(this, "error", f"{name} is end")
		except:
			return False


	def get_debt_usr(self, textInput, info):
		tst = ['ts', 'data']

		for i in info:
			for x in i:
				r = x.split('=')
				
				tst.append(x.strip())

		
		t =QCompleter(tst)
		return textInput.setCompleter(t)\

	def show_bell_doc(self, table):
		row = table.rowCount()
		if row > 0:
			tableInfo = self.fetch_table_info(table)
	
			html =  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
			html += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
			html += "p, li { white-space: pre-wrap; }\n"
			html += "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt; font-weight:600;\">welcome</span></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:22pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">Name            Quantity               Price</span></p>\n"
			html += f"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			#body page start from here
		
			
			total = float(0)
			for i in tableInfo:
				
				
				html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\"> {str(i[1])}                         {i[2]}                       {i[3]}</span></p>\n"
				total +=  float(i[3])
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">       ----------------------------------------------------------</span></p>\n"
			html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">total:                                         {str(total)}</span></p></body></html>"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += f"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">date:  {datetime.datetime.now().ctime()}</p></body></html>"
			doc = PrintDoc(html)
			doc.show_Bell()


	def bellNum(self):
		
		return len(self.sl.fetch_all_sells())


	

	








			


if __name__ == '__main__':
	s = Home_page()
	print(s.updateProductQuantity(152))