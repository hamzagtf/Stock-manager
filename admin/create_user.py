
from .sql_setup import Admin_sql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from .register import Ui_Dialog
from PyQt5.Qt import Qt

class Create_user:
    def __init__(self):
        self.con = Admin_sql()
        self.ui = None

    def user_input(self, this):
        """show dialog box"""
        Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(Dialog)

        Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.ui.admin_role.addItem("Admin")
        self.ui.admin_role.addItem("Seller")
        self.ui.admin_role.currentTextChanged.connect(self.comboBoxData)
        self.ui.checkBox_3.setEnabled(False)
        self.ui.checkBox_2.setEnabled(False)
        self.ui.checkBox.setEnabled(False)
        Dialog.show()
        res = Dialog.exec_()
        #user info
        username = self.ui.Admin_username.text().strip()
        phone = self.ui.admin_phone.text().strip()
        role = self.ui.admin_role.currentText()
        password = self.ui.admin_password.text().strip()
        #if user clicked accept 

        if res == QtWidgets.QDialog.Accepted:
            #insert user to db
            if len(username) != 0 and len(phone) != 0:
                dbt = "true" if self.ui.checkBox_3.isChecked() else 'false'
                settings = "true" if self.ui.checkBox_2.isChecked() else 'false'
                stock = "true" if self.ui.checkBox.isChecked() else 'false'
                self.con.create_user(username, password, phone, role, dbt, settings, stock)
                QMessageBox.information(this, "Info", "User created successfully")

    def comboBoxData(self, val):
       
        if val == "Seller":
            self.ui.checkBox_3.setEnabled(True)
            self.ui.checkBox_2.setEnabled(True)
            self.ui.checkBox.setEnabled(True)
        else:
            self.ui.checkBox_3.setEnabled(False)
            self.ui.checkBox_2.setEnabled(False)
            self.ui.checkBox.setEnabled(False)

    def create(self, username, password, phone, role, dbt, settings, stock):
        self.con.create_user(username, password, phone, role, dbt, settings, stock)


if __name__ == "__main__":
    con = Create_user()
    print(con.create('admin' ,"admin", "0", "admin", 'true', 'true', 'true'))
