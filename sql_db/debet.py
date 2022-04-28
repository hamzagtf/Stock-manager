import datetime
from .db_sql import Connect_db

#create user
#-username
#-
class DebetManager:

	def __init__(self):
		self.db = Connect_db()
		self.table= 'debet_users'


	def createUser(self,bellNum, username, proName, price, quantity, created_at):
		
		return self.db.create_(self.table,
			bellNum=bellNum,
			username=username,
			productName=proName,
			price=price,
			quantity=quantity,
			created_at=created_at
			
			)

 
	def updateDebetUser(self,name, username):
		try:
			con = f"username='{name}'"
			self.db.update_(self.table,
				con,
				username=username)
			return True 
		except Exception as e:
			raise e


	def deleteDebetUser(self,username):
		u_id = f'username="{username}"'
		return self.db.delete_(self.table, u_id)
	
	def deleteDebetUserBell(self,bellNum):
		u_id = f'bellNum="{bellNum}"'
		return self.db.delete_(self.table, u_id)
	

	def fetchDetByBellNumber(self, bellNumber):
		bellNumber = f'bellNum="{bellNumber}"'
		return self.db.fetch_All(self.table, bellNumber)


	def fetchAllUsers(self):
		return self.db.fetch_(self.table)

	def fetchUser(self, u_id):
		username = f'username="{u_id}"'
		return self.db.fetch_All(self.table, username)
	

	def search_in_users(self, **kwargs):
		return self.db.search_(self.table, kwargs)
	
	def fetchNames(self, username):
		return self.db.fecthRow(self.table, 'username',f'username="{username}"')

	def fetchTotal(self, username):
		
		return self.db.fecthRow(self.table, 'price',f'username="{username}"')


	def fetchPrice(self, bellNum):
		bellNum = f"bellNum='{bellNum}'"
		return self.db.fecthRow(self.table, 'price', bellNum)
	

	def fetch_total_debt(self):
		bellNum = self.db.fetch_(self.table)
		return bellNum
	#dbt user table 
	def fetch_Debt_User(self, username):
		data = f"username='{username}'"
		return self.db.fetch_All('debet_users_accounts', data)
	

	def fetch_All_debt_users(self):
		return self.db.fetch_('debet_users_accounts')

	
	def create_debt_usr(self, username, phonenumber):
		if len(self.fetch_Debt_User(username)) == 0:
			created_at= datetime.datetime.now().strftime("%c")
			self.db.create_('debet_users_accounts',
			username=username, 
			phoneNum=phonenumber, 
			created_at=created_at)
			return True 
		else:
			return False
	
	def update_debt_user(self,u_id,  username, phone):
		try:
			if len(username) == 0:
				self.db.update_('debet_users_accounts',
				f'rowid="{u_id}"',
				phoneNum=phone)
			elif phone == 0:
				self.db.update_('debet_users_accounts',
				f'rowid="{u_id}"',
				username=username,
				)
			else:
				self.db.update_('debet_users_accounts',
				f'rowid="{u_id}"',
				username=username,
				phoneNum=phone)
			return True
		except Exception as e:
			raise e


	def delete_dbt_user(self, username):
		u_id = f"username='{username}'"
		return self.db.delete_('debet_users_accounts', u_id)






if __name__ == '__main__':
	con = DebetManager()
	print(con.fetch_All_debt_users())
	print(con.deleteDebetUser('hamza'))
	print(con.fetchAllUsers())