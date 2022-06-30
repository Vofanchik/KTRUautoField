from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5 import QtGui, QtWidgets
from inface import Ui_MainWindow

import EISparse
import DocxFiller
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.item_count = 0
        self.r = EISparse.ParseKTRU()
        self.d = DocxFiller.DocxForm()
        self.ui = Ui_MainWindow()
        self.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search_ktru)
        self.ui.pushButton_2.clicked.connect(self.add_position)
        self.ui.pushButton_3.clicked.connect(self.save_docx)
        self.ui.comboBox_3.activated[str].connect(self.onChanged_combobox3)
        self.ui.comboBox_2.activated[str].connect(self.onChanged_combobox2)

        self.ui.tableWidget.resizeColumnsToContents()

        self.fnt = self.ui.tableWidget.font()
        self.fnt.setPointSize(8)
        self.fnt.setUnderline(False)
        self.ui.tableWidget.setFont(self.fnt)

    def search_ktru(self):
        self.ktru = self.ui.lineEdit.text()

        try:
            self.ui.comboBox_3.clear()
            self.ui.comboBox_2.clear()
            self.id_ktru = self.r.get_response(self.ktru)
            self.info = self.r.get_common_info(self.id_ktru)
            self.ui.textEdit_4.setPlainText(self.info['name'])
            self.ui.lineEdit_3.setText(self.info['measure'])

            self.ui.pushButton_4.setStyleSheet('background: rgb(255,255,255);')
            self.ui.pushButton_5.setStyleSheet('background: rgb(255,255,255);')

            if len(list(self.info['nkmi'].items()))>1:
                self.ui.pushButton_4.setStyleSheet('background: rgb(255,0,0);')

            if len(list(self.info['okpd'].items()))>1:
                self.ui.pushButton_5.setStyleSheet('background: rgb(255,0,0);')

            for i in list(self.info['nkmi'].items()):
                self.ui.comboBox_3.addItem(i[0])

            for i in list(self.info['okpd'].items()):
                self.ui.comboBox_2.addItem(i[0])

            self.ui.textEdit_2.setPlainText(self.info['nkmi'][f'{self.ui.comboBox_3.currentText()}'][1])
            self.ui.textEdit.setPlainText(self.info['okpd'][f'{self.ui.comboBox_2.currentText()}'])
            self.ui.textEdit_3.setPlainText(self.info['nkmi'][f'{self.ui.comboBox_3.currentText()}'][0])
            QMessageBox.information(self, "Готово",
                                 "Поиск завершен, теперь уточните подходящий ОКПД, НКМИ и количество", QMessageBox.Ok)

            self.tz = self.r.get_tz_ktru(self.id_ktru)
            if self.tz == None:
                self.tz = {}
            else:
                QMessageBox.information(self, "Характеристики",
                                        f"В ТЗ присутствуют харакетристики, обратите внимание на фразу о их недостаточности",
                                        QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Ошибка поиска", "Введите корректную позицию ктру или проверьте интернет соединение", QMessageBox.Ok)

    def add_position(self):
        try:
            quantity = self.ui.lineEdit_4.text()
            lack_of_description = self.ui.comboBox.currentIndex()
            self.d.common_fill(self.info['name'], self.ui.comboBox_2.currentText(), self.ktru, self.ui.comboBox_3.currentText(), self.info['measure'], quantity)
            self.d.tz_fill(self.info['name'], self.ui.textEdit_2.toPlainText(), lack_of_description,  **self.tz)
            self.ui.tableWidget.setRowCount(self.item_count+1)

            self.ui.tableWidget.setItem(self.item_count, 0, QTableWidgetItem(f"{self.info['name']}"))
            self.ui.tableWidget.setItem(self.item_count, 1, QTableWidgetItem(f"{self.info['measure']}"))
            self.ui.tableWidget.setItem(self.item_count, 2, QTableWidgetItem(f"{quantity}"))
            self.item_count+=1
            QMessageBox.information(self, "Готово",
                                    f"Добавлена позиция {self.info['name']} в количестве {quantity} едениц измерения - {self.info['measure']}",
                                    QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Ошибка добавления", "Попробуйте другую позицию КТРУ", QMessageBox.Ok)

    def save_docx(self):
        try:
            self.d.doc_save()
            QMessageBox.information(self, "Готово",
                                 "Документ сохранен в текущей директории", QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Ошибка сохранения", "Проверьте, не открыт ли фаил с названием ТЗ.docx в текущей директории", QMessageBox.Ok)
    def onChanged_combobox3(self):
        self.ui.textEdit_2.setPlainText(self.info['nkmi'][f'{self.ui.comboBox_3.currentText()}'][1])
        self.ui.textEdit_3.setPlainText(self.info['nkmi'][f'{self.ui.comboBox_3.currentText()}'][0])

    def onChanged_combobox2(self):
        self.ui.textEdit.setPlainText(self.info['okpd'][f'{self.ui.comboBox_2.currentText()}'])


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