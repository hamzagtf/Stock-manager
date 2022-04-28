from .sql_setup import Admin_sql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Fetching_data:
    def __init__(self):
        self.con = Admin_sql()
        
        

    
    def fetch_All_Users(self, table):
        data = self.con.fetch_all_users()
        table.setRowCount(len(data))
        try:
            for index, i in enumerate(data):
                table.setItem(index,0 , QtWidgets.QTableWidgetItem(str(i[0])))#id
                table.setItem(index,1 , QtWidgets.QTableWidgetItem(str(i[1])))#username
                table.setItem(index,2 , QtWidgets.QTableWidgetItem(str(i[3])))#role
                table.setItem(index,3 , QtWidgets.QTableWidgetItem(str(i[4])))#phone
        except Exception as e:
            raise e
    

    def fetch_user_by_name(self, username, password):
        """this function will check if user exist or not"""
        username = self.con.fetch_user_by_name(
            username.text().strip(), 
            password.text().strip())
        if len(username) > 0:
            return username[0]
        else:
            return False
    


        
        
    

    

    

if __name__ == "__main__":
    con = Fetching_data()
    print(con.fetch_user_by_name("",'hamza', "123456789"))

