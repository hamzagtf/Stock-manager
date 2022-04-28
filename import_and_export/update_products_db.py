import requests 
from sql_db.main import Product_manager
from .spinner import Ui_Dialog
from PyQt5 import QtWidgets
import threading
class Update_DB:
	def __init__(self, *args):
		self.username, self.password = args
		self.ui = None
		self.Dialog = None



	def export(self):
		self.Dialog = QtWidgets.QDialog()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self.Dialog)

		self.ui.start.clicked.connect(lambda:threading.Thread(
			target=self.download_file_from_user_account).start()) 

		self.Dialog.show()
		res = self.Dialog.exec_()


	def download_file_from_user_account(self):
		
		url = "https://raw.githubusercontent.com/GuechoudNassim/superette-produit-data-dz/main/json/Stock.json"

		source = requests.get(
		    #"http://127.0.0.1:8000/posts/", 
		    url,
		    #auth=(self.username, self.password),
		    stream=True)

		
		data_length = source.headers['Content-length']
		chunk_size = 1025

		m = 0
		with open("file.json", "wb") as f:

			for i , chunk in enumerate(source.iter_content(chunk_size=chunk_size)):
				#count  downloaded data
				downloaded_data = int(i) * int(chunk_size )/ int(data_length) * 100

				#count the precentge

				precentage = (downloaded_data * 100) / (float(data_length))
				precentage = round(precentage)

				self.ui.start.setEnabled(False)

				self.ui.progressBar.setValue(precentage)

				f.write(chunk)
				m += len(chunk)
			print(data_length)
			print(m)
			


