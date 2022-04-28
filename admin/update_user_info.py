from .sql_setup import Admin_sql
from PyQt5 import QtWidgets
from sql_db import db_sql
from PyQt5.QtWidgets import QMessageBox
from .register import Ui_Dialog
from .index import Fetching_data
from seller import Sells
from PyQt5.Qt import Qt
class Update_user_info:

    def __init__(self):
        self.con = Admin_sql()
        self.ui = None
    
    def update_user(self, this):
        """show dialog box"""
        table = this.ui.table_user
        row = table.currentRow()
        if row >=  0:
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            self.ui = ui
            ui.admin_role.addItem("Admin")
            ui.admin_role.addItem("Seller")

            #old info of user
            user_id = table.item(row, 0).text()
            old_user_name = table.item(row,1).text()
            old_phone = table.item(row,2).text()
            old_role = table.item(row,3).text()
            #set inputs to old info

            ui.Admin_username.setText(old_user_name)
            ui.admin_phone.setText(old_phone)
            ui.admin_role.setCurrentText(old_role)

            #combo box
            self.ui.admin_role.currentTextChanged.connect(self.comboBoxData)

            states = False
            if old_role == "Seller":
                states = True

            self.ui.checkBox_3.setEnabled(states)
            self.ui.checkBox_2.setEnabled(states)
            self.ui.checkBox.setEnabled(states)

            Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
            Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)



            Dialog.show()
            res = Dialog.exec_()
            #user info
            username = ui.Admin_username.text().strip()
            phone = ui.admin_phone.text().strip()
            role = ui.admin_role.currentText()
            password = ui.admin_password.text().strip()
            #if user clicked accept 

            if res == QtWidgets.QDialog.Accepted:
                #if password does't updated
                if len(password) == 0:
                    dbt = "true" if self.ui.checkBox_3.isChecked() else 'false'
                    settings = "true" if self.ui.checkBox_2.isChecked() else 'false'
                    stock = "true" if self.ui.checkBox.isChecked() else 'false'

                    updates = self.con.update_user(user_id, username=username, phone=phone, role=role,
                     dbt=dbt, settings=settings, stock=stock)
                    
                else:
                    
                    updates = self.con.update_user(user_id, 
                    username=username,
                    password=password, 
                    phone=phone, 
                    role=role)
                    updates = True
                
                if updates:

                    #update selles username too
                    db_sql.Connect_db().update_(
                    "sells", 
                    f"username='{username}'", 
                    username=username)

                    #update the table
                    Fetching_data().fetch_All_Users(table)

                    QMessageBox.information(this, 'Info', "success!")
                else:
                    raise Exception

    def comboBoxData(self, val):
        states = False
       
        if val == "Seller":
            states = True
            
        self.ui.checkBox_3.setEnabled(states)
        self.ui.checkBox_2.setEnabled(states)
        self.ui.checkBox.setEnabled(states)
    

    def delete_user(self,this, table):
        row = table.currentRow()
        if row >= 0:
            user_id = table.item(row, 0).text()
        
            if self.con.delete_user(user_id):
                QMessageBox.information(this, 'Info', "success!")
                table.removeRow(row)
            else:
                QMessageBox.warning(this, "Error", "Error")





