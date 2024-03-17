import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import *
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

import sys
from PySide6.QtWidgets import *
from budgetview import CustomTable
from datetime import datetime

class Bookkeeeper(QWidget):
    def __init__(self):
        super().__init__()
        # Создаем вторую таблицу для суммы и бюджета по дням
        self.daily_table = CustomTable(3, 3)
        self.daily_table.set_table_header(['Сумма', 'Бюджет', 'Разница'])
        self.daily_table.set_row_labels(['День', 'Месяц', 'Год'])

        self.sqlite_manager = SQLiteManager('expence3.db')
        self.init_ui()





    def init_ui(self):
        self.setWindowTitle('The Bookkeeeper App')
        layout = QVBoxLayout()

        self.label = QLabel("Последние расходы")
        layout.addWidget(self.label)

        # Создание таблицы для отображения данных
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)  # Скрыть названия строк
        self.table.verticalHeader().setMinimumWidth(0)  # Установить минимальную ширину названий строк
        self.table.verticalHeader().setDefaultSectionSize(25)  # Установить фиксированную высоту строк
        layout.addWidget(self.table)


        self.label = QLabel("Бюджет")
        layout.addWidget(self.label)

        self.table_widget = QTableWidget(3, 3)  # Создание таблицы 3x3
        # Для автоматического растяжения таблицы по высоте виджета
        self.table_widget.setFixedHeight(150)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_widget)

        #layout.addWidget(self.label)
        #layout.addWidget(self.daily_table)

        # Создание кнопки для добавления данных
        # Добавляем виджеты для выбора категорий, ввода суммы и кнопки "Add"
        category_combo = QComboBox()
        category_combo.addItems(['Категория 1', 'Категория 2', 'Категория 3'])  # Замените на свои категории
        amount_edit = QLineEdit()

        layout.addWidget(category_combo)
        layout.addWidget(amount_edit)

        add_button = QPushButton('Add Expense')
        add_button.clicked.connect(lambda: self.add_expense_big(category_combo, amount_edit))
        layout.addWidget(add_button)

        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        # Создаем кнопки
        button1 = QPushButton("Убрать последнию расходы")
        button2 = QPushButton("Delet base")

        button1.clicked.connect(self.Delet_Last)
        button2.clicked.connect(self.Delet_Base)
        # Добавляем кнопки в горизонтальный layout
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        layout.addLayout(button_layout)
        #button2.clicked.connect(self.Delet_Base)
        self.setLayout(layout)


        self.expense_changes()
        self.buget_changes()



    #ДЛЯ РАБОТЫ С ТАБЛИЦОЙ РАСХОДВ
    def expense_changes(self):
        # Проверяем наличие таблицы 'Expence' и создаем ее, если она отсутствует
        self.sqlite_manager.execute_query("CREATE TABLE IF NOT EXISTS expence (id INTEGER PRIMARY KEY, date TEXT, amount REAL, category TEXT, comment TEXT)")


        data = self.sqlite_manager.fetch_data("SELECT date, amount, category, comment FROM expence")

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]) if data else 0)

        header_labels = [description[0] for description in self.sqlite_manager.cursor.description]
        self.table.setHorizontalHeaderLabels(header_labels)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_num, col_num, item)

        # Установка размеров таблицы для заполнения всей доступной высоты окна
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Связываем изменения в ячейках таблицы с обновлением данных в базе данных
        self.table.itemChanged.connect(self.update_data_in_expence)


    def buget_changes(self):
        self.sqlite_manager.execute_query("CREATE TABLE IF NOT EXISTS Budget (id INTEGER PRIMARY KEY, column1 TEXT, column2 TEXT, column3 TEXT)")

        row_count = self.sqlite_manager.fetch_data("SELECT COUNT(*) FROM Budget")[0][0]
        # Добавление пустых строк, если их меньше 3
        while row_count < 3:
            self.sqlite_manager.execute_query(
                "INSERT INTO Budget (column1, column2, column3) VALUES ('', '', '')")
            row_count += 1

        #--------------------
        # Получение всех значений из столбца amount в таблице expence
        fetch_query = "SELECT amount FROM expence"
        amounts = self.sqlite_manager.fetch_data(fetch_query)

        # Суммирование только числовых значений
        total_sum = 0
        for amount in amounts:
            try:
                # Пытаемся преобразовать значение в число и прибавить его к общей сумме
                total_sum += float(amount[0])
            except ValueError:
                # Если не удалось преобразовать в число, пропускаем это значение
                continue

        # Обновляем первый столбец в таблице Budget, где id = 2, значением суммы
        update_query = f"UPDATE Budget SET column1 = {total_sum} WHERE id = 2"
        self.sqlite_manager.execute_query(update_query)

        #-----------
        # Обновляем первый столбец в таблице Budget, где id = 2, значением суммы
        for i in range(3):
            try:
                update_query = f"UPDATE Budget SET column3 = column2 - column1  WHERE id = {i+1}"
                self.sqlite_manager.execute_query(update_query)
            except ValueError:
                # Если не удалось преобразовать в число, пропускаем это значение
                continue

        # Получение всех значений из двух столбцов в таблице expence
        fetch_query = "SELECT column1 FROM budget"
        amounts = self.sqlite_manager.fetch_data(fetch_query)

        # Суммирование значений из двух столбцов

        for amount1 in amounts:
            print(amount1, "{{{")
            """
            #try:
                # Пытаемся преобразовать значения в числа и прибавить их к общей сумме
                total_sum = float(amount1) + float(amount2)
                # Обновляем первый столбец в таблице Budget, где id = 2, значением суммы
                update_query = f"UPDATE Budget SET column1 = {total_sum} WHERE id = 2"
                self.sqlite_manager.execute_query(update_query)

            #except ValueError:
                # Если не удалось преобразовать в число, пропускаем это значение
            #    continue
            """
        #--------------

        data = self.sqlite_manager.fetch_data("SELECT column1, column2, column3 FROM Budget")



        # Установка названий строк и столбцов
        row_headers = ['Row 1', 'Row 2', 'Row 3']
        column_headers = ['column1', 'column2', 'column3']
        self.table_widget.setVerticalHeaderLabels(row_headers)
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        # Заполнение таблицы данными из базы данных
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                # Установка цвета текста в зависимости от значения
                try:
                    if col_num == 2 and float(col_data) > 0:  # Предполагается, что третий столбец содержит числа
                        item.setForeground(QColor('green'))
                    elif col_num == 2 and float(col_data) < 0:
                        item.setForeground(QColor('red'))
                except ValueError:
                    pass
                self.table_widget.setItem(row_num, col_num, item)

        # Установка размеров таблицы для заполнения всей доступной высоты окна
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Связываем изменения в ячейках таблицы с обновлением данных в базе данных
        self.table_widget.itemChanged.connect(self.update_data_in_budget)

    #ДЛЯ ИЗМЕНЕНИЯ БАЗЫ ДАННЫХ ПРИ ИЗМЕНЕНИЕЕ ТАБЛИЦЫ
    def update_data_in_expence (self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        print(new_value)
        print(row)

        id_value = row +1

        column_name = self.table.horizontalHeaderItem(col).text()
        print(column_name)
        query = f"UPDATE Expence SET {column_name} = '{new_value}' WHERE id = {id_value}"
        print(query)

        self.sqlite_manager.execute_query(query)
        self.buget_changes()

    def update_data_in_budget (self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        print(new_value)
        print(row)

        id_value = row + 1

        column_name = self.table_widget.horizontalHeaderItem(col).text()
        print(column_name)
        query = f"UPDATE Budget SET {column_name} = '{new_value}' WHERE id = {id_value}"
        print(query)

        self.sqlite_manager.execute_query(query)


    def add_expense_big (self, category, amount):
        # Добавление новой записи в таблицу
        # Здесь можно добавить диалоговое окно для ввода данных
        self.sqlite_manager.execute_query(f"INSERT INTO expence (date, amount, category, comment) VALUES ('{datetime.now().date()}', '{amount.text()}', '{category.currentText()}', 'Lunch')")
        # Обновление отображаемых данных в таблице
        # Связываем изменения в ячейках таблицы с обновлением данных в базе данных

        self.expense_changes()
        self.buget_changes()

    def Delet_Base(self):
        self.sqlite_manager.execute_query("DELETE FROM expence")
        self.expense_changes()
        self.buget_changes()
    def Delet_Last(self):
        # Получение последней добавленной записи из таблицы expence
        last_expense_id = self.sqlite_manager.fetch_data("SELECT id FROM expence ORDER BY id DESC LIMIT 1")

        if last_expense_id:
            # Удаление записи по идентификатору
            self.sqlite_manager.execute_query(f"DELETE FROM expence WHERE id = {last_expense_id[0][0]}")
            # Обновление отображаемых данных в таблице
            self.expense_changes()
            self.buget_changes()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    expense_app = Bookkeeeper()
    expense_app.show()

    sys.exit(app.exec())
