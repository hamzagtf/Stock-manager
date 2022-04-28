from .fetch_data import Fetching_data
from .create_user import Create_user
from .update_user_info import Update_user_info
from PyQt5.QtWidgets import *
from .connect_user import checkUserOnline


class Admin:
    def __init__(self):
        self.create = Create_user()
        self.update = Update_user_info()
        self.fetch =  Fetching_data()
    
    def create_seller(self, this, table):
        self.create.user_input(this)
        self.fetch_ALL_Users(table)
    

    def update_seller(self, this):
        self.update.update_user(this)
        #self.fetch_ALL_Users(this.ui.table_user)

    

    def delete_seller(self, this, table):
        self.update.delete_user(this, table)

    
    
    def fetch_ALL_Users(self, table):
        self.fetch.fetch_All_Users(table)

    
    def check_user_login(self, this, ui):
        user =  ui.email
        password = ui.password
        
        sideBar = ui.sideBar
        page = ui 
        page_num = ui.page

        #check if user is exist

        username = self.fetch.fetch_user_by_name( user, password)
        
        if username:

            user_name = username[1]
            role = username[4]
            
            sideBar.show()
            page.stackedWidget.setCurrentWidget(page_num)


            #set the role of seller
            if role.lower() == "admin":
                ui.SETTINGS.show()
                ui.STOCK.show()
                ui.DEBT.show()

            if username[5] == 'false':
                ui.DEBT.hide()

            if username[6] == 'false':
                ui.SETTINGS.hide()

            if username[7] == 'false':
                ui.STOCK.hide()





            PASSWORD= password.text()
            user.setText('')
            password.setText("")
        
            return (user_name, PASSWORD , role)
            
        else:
            QMessageBox.warning(this, "error", "ﻻيوجد هذا اﻻسم")


        

