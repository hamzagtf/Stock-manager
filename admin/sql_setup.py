from sql_db.db_sql import Connect_db
import datetime


class Admin_sql:
    """this class handle all sql functions 
    that relate to admin table"""

    
    def __init__(self):
        self.con = Connect_db()
        self.table = "admin"


    def create_user(self, username, password, phone, role, dbt, settings, stock):
        created_at = datetime.datetime.now().strftime("%c")
        try:
            self.con.create_(self.table,username=username, 
            password=password,
            phone=phone, 
            role=role, 
            dbt=dbt,
            settings=settings,
            stock=stock,
            created_at=created_at) 
            return True
        except Exception as e:
            raise e
    
    def update_user(self,userid, **kwargs):
        condition = f"rowid = '{userid}'"
        
       
        try:
            
            if len(kwargs) >= 4: 
            
                self.con.update_(self.table,condition,
                username=kwargs.get("username"),
                password=kwargs['password'],
                phone=kwargs.get("phone"),
                role=kwargs.get("role")
                )
            else:
                self.con.update_(self.table,condition,
                username=kwargs.get("username"),
                phone=kwargs.get("phone"),
                role=kwargs.get("role")
                )

                
                return True
            
        except Exception as e:
            raise e

    def fetch_user_by_name(self, user_name, password):
        """this function rtrn a list within a tuple
        which fetch useri info by name"""


        condition = f"username='{user_name}' AND password='{password}'"
        try:
            return self.con.fetch_All(self.table, condition)
        except Exception as e:
            raise e
    
    def fetch_user_role(self, user_id):

        """this function rturn the role of 
        user by it's own id"""

        user_role = self.fetch_user_by_id(user_id)
        if len(user_role) > 0:
            return user_role[0][3] #fetch user role

    def fetch_all_users(self):
        """this function return a list within 
        a tuple of all users inside db"""

        return self.con.fetch_(self.table)
    

    def delete_user(self, user_id):
        try:
            self.con.delete_(self.table, user_id)
            return True
        except Exception as e: 
            raise e


if __name__ == "__main__":
    con = Admin_sql()
    print(con.create_user('hamza' ,'123456', "1254", 'admin'))
    print(con.fetch_all_users())

    
        

