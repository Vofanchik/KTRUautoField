from PyQt5 import QtWidgets
from inface import Ui_MainWindow
import sys


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)

    def btnClicked(self):
        self.ui.label.setText('Button clicked')
        self.ui.label.adjustSize()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())