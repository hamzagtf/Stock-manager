from PyQt5 import  QtWidgets
from printdoc_ import  Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
class PrintDoc(QMainWindow):
    def __init__(self, html):

        QMainWindow.__init__(self)
        self.ui = Ui_Form(html)
        self.ui.setupUi(self)
    

    def printfile(self):
        printer = QPrinter(QPrinter.HighResolution)
        d = QPrintDialog(printer, self)
        if d.exec_() == QPrintDialog.Accepted:
        #add table data
            self.ui.pdfDoc.print_(printer)
    
    def show_Bell(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setResolution(60) #set the width of the page
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.text)
        preview.exec_()
	

    def text(self, printer):
        self.ui.pdfDoc.print_(printer)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = PrintDoc()
    ui.show()
    #MainWindow
    sys.exit(app.exec_())
