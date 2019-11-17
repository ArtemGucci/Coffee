from sys import argv, exit
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QTableWidgetItem, QWidget
import sqlite3


COLUMNS = ['title', 'deg', 'way', 'taste', 'price', 'volume']


class Coffee(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.flag = False
        self.print.clicked.connect(self.output)
        self.change.clicked.connect(self.add)

    def output(self):
        con = sqlite3.connect('coffee.sqlite.db')
        cur = con.cursor()
        sql = """select title from Coffee"""
        names = [i[0] for i in cur.execute(sql).fetchall()]
        i, okBtnPressed = QInputDialog.getItem(self, "Название",
                                            "Выберите название кофе",
                                            names, False)
        if okBtnPressed:
            sql = """SELECT * From Coffee where title = ?"""
            result = cur.execute(sql, (i,)).fetchall()
            self.table.setRowCount(1)
            for i in result:
                for j, elem in enumerate(i):
                    if j:
                        self.table.setItem(0, j - 1, QTableWidgetItem(str(elem)))
            self.table.resizeColumnsToContents()

    def add(self):
        self.widget = addEditCoffeeForm()
        self.widget.show()


class addEditCoffeeForm(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.add.clicked.connect(self.append)
        self.change.clicked.connect(self.changeP)

    def append(self):
        self.result.clear()

        con = sqlite3.connect('coffee.sqlite.db')
        cur = con.cursor()
        edits = [self.title, self.deg, self.way, self.taste, self.price, self.volume]
        values = [i.text() for i in edits]

        sql = """INSERT INTO Coffee(title, deg, way, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)"""
        cur.execute(sql, (values[0], values[1], values[2], values[3], values[4], values[5]))
        con.commit()
        self.result.setText('Успешно!')

    def changeP(self):
        self.result.clear()

        con = sqlite3.connect('coffee.sqlite.db')
        cur = con.cursor()
        sql = """select title from Coffee"""
        names = [i[0] for i in cur.execute(sql).fetchall()]
        i, okBtnPressed = QInputDialog.getItem(self, "Название",
                                               "Выберите название кофе",
                                               names, False)
        if not okBtnPressed:
            self.result.setText('Вы не выбрали название')
            return

        name = i
        edits = [self.title, self.deg, self.way, self.taste, self.price, self.volume]
        sql = """UPDATE Coffee SET {} = ? WHERE title = ?"""

        for i, edit in enumerate(edits):
            if edit.text():
                sql1 = sql.format(COLUMNS[i])
                cur.execute(sql1, (edit.text(), name))
                con.commit()

        self.result.setText('Успешно!')


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Coffee()
    ex.show()
    exit(app.exec_())