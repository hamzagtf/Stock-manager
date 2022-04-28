from sql_db import debet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from addUserDet import Ui_Dialog as UD
from printDoc import PrintDoc
from PyQt5.Qt import Qt
from pay import Pay

class DebetPage:
	def __init__(self):
		self.db = debet.DebetManager()
		

	def pay(self, this):
		Pay().pay(this)


	def fetch_All_Users(self, this, table):
		self.total(this.ui.d_total)
		info = self.db.fetchAllUsers()
		table.setRowCount(len(info))
		row = 0
		
		bells_number = []
		#print(info)

		for i in info:
			
			if i[2] not in bells_number:
				total = self.count_user_price(i[2])
				table.setItem(row, 0, QtWidgets.QTableWidgetItem(i[1]))
				table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))
				table.setItem(row, 2, QtWidgets.QTableWidgetItem(total))
				table.setItem(row, 3, QtWidgets.QTableWidgetItem(i[6]))
				bells_number.append(i[2])
				row = row + 1

		table.setRowCount(len(bells_number))


	def search_In_Users(self, keyword, table):
		keywords = keyword.text().strip()
		keyWordResult = self.db.search_in_users(username=keywords)
		row = 0
		table.setRowCount(len(keyWordResult))
		bells_number = []
		#print(info)

		for i in keyWordResult:
			
			if i[2] not in bells_number:
				total = self.count_user_price(i[2])
				table.setItem(row, 0, QtWidgets.QTableWidgetItem(i[1]))
				table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))
				table.setItem(row, 2, QtWidgets.QTableWidgetItem(total))
				table.setItem(row, 3, QtWidgets.QTableWidgetItem(i[6]))
				bells_number.append(i[2])
				row = row + 1

		table.setRowCount(len(bells_number))


			

	def removeUser(self,this,table, lcd):
		if table.rowCount() >= 0:
			row = table.currentRow()
			if row >= 0:
				username = table.item(row, 1).text()
				val = table.item(row, 2).text()
				x = lcd.value() -  float(val)
				lcd.display(x)
				self.db.deleteDebetUser(username)
				self.db.delete_dbt_user(username)
				Pay().deleteUser(username)
				table.removeRow(row)
				QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
			


	def add_new_dt_user(self, this):
		
		Dialog = QtWidgets.QDialog()
		ui = UD()
		ui.setupUi(Dialog)
		Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
		Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
		
		Dialog.show()
		res = Dialog.exec_()
		if res == QtWidgets.QDialog.Accepted:
			name = ui.d_userName.text().strip()
			phone = ui.d_phoneNum.value()
			if len(name) != 0:
				if self.db.create_debt_usr(name, phone):
					QMessageBox.information(this, 'Info', "تمت العملية بنجاح")
				else:
					QMessageBox.warning(this, 'Error', 'هذا الاسم موجود')	
		else: 
			return False

	
	def total(self, lcd):
		info = self.db.fetch_total_debt()

		price =float( 0)
		for i in info:
			price += float(i[4])
		
		lcd.display(price)


	def showBook(self, page, pgNum, main_table, subTable,u_name, phone, number):
		row = main_table.currentRow()
		if row >= 0 :
			username = main_table.item(row, 1).text().strip()
			page.setCurrentWidget(pgNum)
			userInfo = self.db.fetch_Debt_User(username)[0]
			
			u_name.setText(userInfo[1])
			phone.setText(userInfo[2])
			number.setText(str(userInfo[0]))
		

			info = self.db.fetchUser(username)
			bells = []
			row = 0
			
			

			subTable.setRowCount(len(info))
			for i in info:
				if i[1] not in bells:
					price = self.count_bell_total(i[1])
					
					subTable.setItem(row,  0, QtWidgets.QTableWidgetItem(i[1]))
					subTable.setItem(row,  1, QtWidgets.QTableWidgetItem(price))
					subTable.setItem(row,  2, QtWidgets.QTableWidgetItem(i[6]))
					bells.append(i[1])
					row += 1
			subTable.setRowCount(len(bells))
	

	def updateUserDtInfo(self,this, number, username, phoneNumber):
		Dialog = QtWidgets.QDialog()
		ui = UD()
		userid = number.text()
		USERNAME = username.text()
		ui.setupUi(Dialog)

		Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
		Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

		Dialog.show()
		res = Dialog.exec_()
		if res == QtWidgets.QDialog.Accepted:

			name = ui.d_userName.text().strip()
			phone = ui.d_phoneNum.value()

			if self.db.update_debt_user(userid, name, phone):
				if len(name) != 0:
					self.db.updateDebetUser(USERNAME, name)

				if len(name) != 0 and phone != 0 :
					username.setText(name)

					phoneNumber.setText(str(phone))
				elif phone == 0:
					username.setText(name)
				elif len(name) == 0:
					phoneNumber.setText(str(phone))

				Pay().updateUserName(username)

				QMessageBox.information(this, 'Info', "تمت العملية بنجاح")
			else:
				QMessageBox.warning(this, 'Error', 'هذا الاسم موجود')	
		else: 
			return False


			
	def removeUserBell(self, this, table):
		if table.rowCount() >= 0:
			row = table.currentRow()
			if row >= 0:
				bellNumber = table.item(row, 0).text()
				self.db.deleteDebetUserBell(bellNumber)
				table.removeRow(row)
				QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
	

	def showUserDbtBell(self, table):
		row = table.currentRow()
		if row >= 0:
	
			html =  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
			html += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
			html += "p, li { white-space: pre-wrap; }\n"
			html += "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt; font-weight:600;\">welcome</span></p>\n"
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:22pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">price                   quantity                      date</span></p>\n"
			html += f"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			#body page start from here
		
			bell_number = table.item(row, 0).text()
			products = self.db.fetchDetByBellNumber(bell_number)
			total = 0
			
			for i in products:
				
				
				html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\"> {i[4]}                     {i[5]}                         {i[6]}</span></p>\n"
				total +=  float(i[4])
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">       ----------------------------------------------------------</span></p>\n"
			html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">total:                                         {str(total)}</span></p></body></html>"
			doc = PrintDoc(html)
			doc.show_Bell()

	def count_user_price(self , username):
		prices = self.db.fetchTotal(username)
		amount = Pay().fetch_amount(username)
		p = 0
		for price in prices:
			p += float(price[0])
		if amount != None:
			p = float(p) - float(amount)
			p = float(0) if p <=0 else p
		return str(p)


	def count_bell_total(self, bell_number):
		
		prices = self.db.fetchPrice(bell_number)
		
		p = 0
		for price in prices:
			p += float(price[0])
		
		return str(p)










if __name__ == '__main__':
	d = DebetPage()
	#d.create_User('username', 'proName', 'price', 'quantity')

	print(d.count_user_price('omar'))






