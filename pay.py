from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from sql_db import db_sql
from quantity import Ui_Dialog 
from PyQt5.Qt import Qt
class Pay:
    def pay(self, this):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        Dialog.show()
        res = Dialog.exec_()
        


        if res == QtWidgets.QDialog.Accepted:
            
            amount = ui.lineEdit.text().strip()
            
            username = this.ui.u_page_name.text()

            if amount.isdigit():
                if self.create_or_update(username=username, amount=amount):
                    QMessageBox.information(this, "info", "Success")
                else:
                    QMessageBox.warning(this, "Error", "Error")

    
    def create_or_update(self, **kwargs):
        username = kwargs['username']
        amount = kwargs['amount']
        sql = db_sql.Connect_db()
        table = 'pay'
        condition = f"username='{username}'"
        created_at = datetime.now().strftime("%c")

        try:
            #check user existence 
            fetch = sql.fetch_All(table, condition)
            if len(fetch) == 0:
                #create user if not exist
                sql.create_(table, username=username, pay=amount, created_at=created_at)

            else:
                #update amount if user exist
                amount = float(fetch[0][2]) + float(amount)
                amount = float(0) if amount <= 0 else amount
                sql.update_(table, condition, pay=amount)
            return True
            
        except Exception as e:
            raise e
    

    def fetch_amount(self, username):
        sql = db_sql.Connect_db()
        table = 'pay'
        condition = f"username='{username}'"
        fetch = sql.fetch_All(table, condition)
        if len(fetch) > 0:
            return fetch[0][2]


    def deleteUser(self, username):
        sql = db_sql.Connect_db()
        table = 'pay'
        condition = f"username='{username}'"
        return sql.delete_(table, condition)


    def updateUserName(self, username):
        sql = db_sql.Connect_db()
        table = 'pay'
        condition = f"username='{username}'"
        return sql.update_(table, condition, username=username)






if __name__ == "__main__":
    con = Pay()
    #print(con.create_or_update(username='hamza', amount="16"))
    print(con.fetch_amount('hamza'))

    




