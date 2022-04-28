from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from .barCode_ import Ui_Dialog
from .generater import genrateBarCode, generate_random_barcode
from .setup import number_Of_Copies
from PyQt5.Qt import Qt
import os
class Barcode:
    def generate_Bar_Code(self):
        
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        image = ui.barcodeInput.textChanged.connect(lambda:self.showBarCode(ui))
        ui.auto_generate.stateChanged.connect(lambda x: self.auto_generate(ui, x))
        Dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        Dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
 
        Dialog.show()
        res = Dialog.exec_()
        

        if res == QtWidgets.QDialog.Accepted:
            self.save_barcode_image(ui)
    

    def showBarCode(self, this):
        barcode = this.barcodeInput.text().strip()
        
        imageContainer = this.barcode_container
        barcodeImage = genrateBarCode(barcode)

        pixmap = QPixmap(barcodeImage)
        imageContainer.setPixmap(pixmap)
        imageContainer.resize(pixmap.width(),
                          pixmap.height())



    def save_barcode_image(self, this):
        copiesNumber = this.spinBox_2.value()
        image_name = "default.png"
        number_Of_Copies(image_name, copiesNumber)
        os.remove(image_name)
    

    def auto_generate(self, this,  state):
        if state == 2:
            this.barcodeInput.setText(str(generate_random_barcode()))
        else:
            this.barcodeInput.setText("")










