import threading
import json
from sql_db import main 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from .spinner import Ui_Dialog
from openpyxl import Workbook



class ExportDB:
    def __init__(self):
        self.con = main.Product_manager()
        self.ui = None
        self.products = self.con.fetch_all_products()
        self.Dialog = None

    def _prograssBarInfo(self, val):
        self.ui.progressBar.setValue(val)
        if self.ui.progressBar.value() == 100:
            self.Dialog.close()

    def prograssBarInfo(self):
        self.threadClass = ThreadClass(parent=None)
        self.threadClass.start()
        self.threadClass.any_signal.connect(self._prograssBarInfo)


    def export(self):
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)

        
        self.prograssBarInfo()
        self.Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.Dialog.show()
        self.ui.start.hide()
        res = self.Dialog.exec_()

 
class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

        self.con = main.Product_manager()
        self.products = self.con.fetch_all_products()
        self.wb = Workbook(write_only=True)
        self.ws = self.wb.create_sheet()


    def run(self):
        self.ws.append([ 
            "reference", "name", " quantity",
            'buy', 'sell', "expired"
            ])

        for i, value in enumerate(self.products, 1):
            percentage = (i * 100 ) / len(self.products)
            self.ws.append([
                value[1], value[2], value[4],
                value[3], value[5], value[6]
                ])

            self.any_signal.emit(percentage)

        self.wb.save('Stock_.xlsx')






