from sql_db import main, debet, sells
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from printDoc import PrintDoc
class Sells:
	def __init__(self):
		self.sl = sells.Sells_Manager()
		

	def fetchAllSells(self, table, *args):
		#check the role of user and fetch data
		if args[1] == 'admin':
			info = self.sl.fetch_all_sells()
		else:
			table.setRowCount(0)
			info = self.sl.fetch_products_by_seller(args[0])

		row = 0
		bells_number = []
		
		if len(info) != 0:
			table.setRowCount(len(info))
			for i in info:
				if i[1] not in bells_number:
					table.setItem(row, 0, QtWidgets.QTableWidgetItem(i[1]))
					table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))
					table.setItem(row, 2, QtWidgets.QTableWidgetItem(i[6]))
					bells_number.append(i[1])
					row = row +1 
			table.setRowCount(len(bells_number))


	def search_in_sells(self, keyword, table, *args):
		keywords = keyword.text().strip()
		keyWordResult = self.sl.search_in_sells(username=keywords, bell_num=keywords,)
		row = 0
		
			
	
		
		bells_number = []
		if len(keyWordResult) != 0:
			if args[1] == 'admin':
				keyWordResult = self.sl.search_in_sells(username=keywords, bell_num=keywords,)
			else:
				keyWord = self.sl.search_in_sells(username=keywords, bell_num=keywords,)
				keyWordResult = [key for key in keyWord if key[2] == args[0]]

				
			table.setRowCount(len(keyWordResult))
			for i in keyWordResult:
				if i[1] not in bells_number:
					table.setItem(row, 0, QtWidgets.QTableWidgetItem(i[1]))
					table.setItem(row, 1, QtWidgets.QTableWidgetItem(i[2]))
					table.setItem(row, 2, QtWidgets.QTableWidgetItem(i[6]))
					row = row +1 
					bells_number.append(i[1])
			table.setRowCount(len(bells_number))


	def removeProduct(self,this, table):
		#need to delete fom db 
		if table.rowCount() > 0:
			row = table.currentRow()
			bell_number = table.item(row, 0).text()
			
			if row >= 0:
				if self.sl.delete_product_(bell_number):
					QMessageBox.information(this, 'Info', 'تمت العملية بنجاح')
					table.removeRow(row)
				else:
					QMessageBox.warning(this, 'Error', 'Error')


	def showBell(self, table):
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
			products = self.sl.fetch_products_(bell_number)
			total = float(0)
			for i in products:
				
				
				html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\"> {i[4]}                     {i[5]}                         {i[6]}</span></p>\n"
				total +=  float(i[4])
			html += "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt; font-weight:600;\"><br /></p>\n"
			html += "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">       ----------------------------------------------------------</span></p>\n"
			html += f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">total:                                         {str(total)}</span></p></body></html>"
			doc = PrintDoc(html)
			doc.show_Bell()





			