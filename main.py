import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem, QTableView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import uic
import sqlite3


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("cofee.sqlite")
        self.pushButton.clicked.connect(self.select_data)
        # По умолчанию будем выводить все данные из таблицы films
        self.textEdit.setPlainText("SELECT * FROM films")
        self.select_data()

    def select_data(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = "SELECT * FROM films"
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        view = self.tableView
        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)

        self.setWindowTitle('Пример работы с QtSql')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
