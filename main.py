from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from inface import Ui_MainWindow
import sys
import EISparse
import DocxFiller


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.r = EISparse.ParseKTRU()
        self.d = DocxFiller.DocxForm()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search_ktru)
        self.ui.pushButton_2.clicked.connect(self.add_position)
        self.ui.pushButton_3.clicked.connect(self.save_docx)

    def search_ktru(self):
        self.ktru = self.ui.lineEdit.text()

        try:
            self.id_ktru = self.r.get_response(self.ktru)
            self.info = self.r.get_common_info(self.id_ktru)
            self.ui.lineEdit_2.setText(self.info['name'])
            self.ui.lineEdit_3.setText(self.info['measure'])
        except:
            QMessageBox.critical(self, "Ошибка ", "Введите корректную позицию ктру", QMessageBox.Ok)



    def add_position(self):
        self.tz = self.r.get_tz_ktru(self.id_ktru)
        if self.tz == None:
            self.tz = {}
        quantity = self.ui.lineEdit_4.text()
        lack_of_description = self.ui.comboBox.currentIndex()
        self.d.common_fill(self.info['name'], list(self.info['okpd'].keys())[0], self.ktru, self.info['measure'], quantity)
        self.d.tz_fill(self.info['name'], list(self.info['nkmi'].values())[0][1],lack_of_description,  **self.tz)

    def save_docx(self):
        self.d.doc_save()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
# ktru = '32.50.13.190-00007224'
# ktru2 = '32.50.13.110-00004585'
# ktru3 = '32.50.30.110-00000142'
#
# r = EISparse.ParseKTRU()
#
# id_ktru = r.get_response(ktru)
# id_ktru2 = r.get_response(ktru2)
# id_ktru3 = r.get_response(ktru3)
# info = r.get_common_info(id_ktru)
# info2 = r.get_common_info(id_ktru2)
# info3 = r.get_common_info(id_ktru3)
#
# tz = r.get_tz_ktru(id_ktru)
# if tz == None:
#     tz = {}
#
# tz2 = r.get_tz_ktru(id_ktru2)
# if tz2 == None:
#     tz2 = {}
#
# tz3 = r.get_tz_ktru(id_ktru3)
# if tz3 == None:
#     tz3 = {}
#
# d = DocxFiller.DocxForm()
# d.common_fill(info['name'], list(info['okpd'].keys())[0], ktru, info['measure'], '3')
# d.tz_fill(info['name'], list(info['nkmi'].values())[0][1], 'not', **tz)
#
# d.common_fill(info2['name'], list(info2['okpd'].keys())[0], ktru2, info2['measure'], '3')
# d.tz_fill(info2['name'], list(info2['nkmi'].values())[0][1], 'not', **tz2)
#
# d.common_fill(info3['name'], list(info3['okpd'].keys())[0], ktru3, info3['measure'], '3')
# d.tz_fill(info3['name'], list(info3['nkmi'].values())[0][1], 'not', **tz3)
#
# d.doc_save()