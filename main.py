from PyQt5 import QtWidgets
from inface import Ui_MainWindow
import sys
import EISparse
import DocxFiller


# class mywindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(mywindow, self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.pushButton.clicked.connect(self.btnClicked)
#
#     def btnClicked(self):
#         self.ui.label.setText('Button clicked')
#         self.ui.label.adjustSize()
#
#
# app = QtWidgets.QApplication([])
# application = mywindow()
# application.show()
#
# sys.exit(app.exec())
ktru = '32.50.13.190-00007224'
ktru2 = '32.50.13.110-00004585'
r = EISparse.ParseKTRU()
id_ktru = r.get_response(ktru)
id_ktru2 = r.get_response(ktru2)
info = r.get_common_info(id_ktru)
info2 = r.get_common_info(id_ktru2)

tz = r.get_tz_ktru(id_ktru)
if tz == None:
    tz = {}

tz2 = r.get_tz_ktru(id_ktru2)
if tz2 == None:
    tz2 = {}

d = DocxFiller.DocxForm()
d.common_fill(info['name'], list(info['okpd'].keys())[0], ktru, info['measure'], '3')
d.tz_fill(info['name'], list(info['nkmi'].values())[0][1], 'not', **tz)

d.common_fill(info2['name'], list(info2['okpd'].keys())[0], ktru2, info2['measure'], '3')
d.tz_fill(info2['name'], list(info2['nkmi'].values())[0][1], 'not', **tz2)

d.doc_save()