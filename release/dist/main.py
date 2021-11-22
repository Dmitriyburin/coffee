import sys
import time
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem, QMessageBox
from PyQt5.QtWidgets import QApplication, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3

from UI.main_ui import Ui_Form
from UI.addEditCoffeeForm import Ui_Form2


class Main(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.change)
        self.pushButton.clicked.connect(self.change)
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        self.setWindowTitle('Пример работы с QtSql')

    def change(self):
        rows = list(map(str, list(set([i.row() for i in self.tableWidget.selectedItems()]))))
        if len(rows) != 0:
            self.change_w = Change(rows)
            self.change_w.setWindowModality(Qt.ApplicationModal)
            self.change_w.show()


class Change(QWidget, Ui_Form2):
    def __init__(self, rows):
        super().__init__()
        self.initUI(rows)

    def initUI(self, rows):
        self.setupUi(self)
        self.modified = {}
        self.titles = None
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.createButton.clicked.connect(self.create_coffee)
        self.price.setMaximum(1000000)
        self.amount.setMaximum(1000000)
        self.rows = rows
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.rows = rows
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id IN ({})".format(
            ', '.join(rows))).fetchall()
        self.titles = [description[0] for description in cur.description]

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                item = QTableWidgetItem(str(val))
                if j == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
        self.modified = {}
        self.setWindowTitle('Пример работы с QtSql')

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()
        # print(len(self.modified), [i for i in self.modified.keys()][0], self.modified)
        if len(self.modified) == 1 and [i for i in self.modified.keys()][0] != 'ID':
            button = QMessageBox.question(self, "Вопрос", "Вы точно хотите изменить значение?")
            if button == QMessageBox.Yes:
                if self.modified:
                    cur = self.con.cursor()
                    que = "UPDATE coffee SET\n"
                    que += ", ".join([f"{key}='{self.modified.get(key)}'"
                                      for key in self.modified.keys()])
                    que += " WHERE id = {}".format(self.tableWidget.item(item.row(), 0).text())
                    print(que)
                    print(self.modified)
                    cur.execute(que)
                    self.con.commit()
                    self.modified.clear()

    def create_coffee(self):

        try:
            print('ok')
            sort_name = self.sort.text() if len(self.sort.text()) != 0 else None
            st = self.combo_1.currentText()
            v = self.combo_2.currentText()
            taste = self.taste.text() if len(self.taste.text()) != 0 else None
            price = self.price.text()
            amount = self.amount.text()
            cur = self.con.cursor()
            if sort_name is not None and taste is not None:
                que = 'INSERT INTO coffee (sort_name, degree_roasting, grains_type, taste, price, amount)'\
                      'VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(sort_name, st, v, taste, price, amount)
                print(que)
                cur.execute(que)
                self.con.commit()
                QMessageBox.information(self, 'Информация', 'Успешно добавлено!')
        except Exception as error:
            print(error)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
