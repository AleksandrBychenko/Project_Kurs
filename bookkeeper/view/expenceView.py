import sys
from PySide6.QtWidgets import *
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

import sys
from PySide6.QtWidgets import *
from budgetview import CustomTable

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        # Создаем вторую таблицу для суммы и бюджета по дням
        self.daily_table = CustomTable(3, 3)
        self.daily_table.set_table_header(['Сумма', 'Бюджет', 'Разница'])
        self.daily_table.set_row_labels(['День', 'Месяц', 'Год'])

        self.sqlite_manager = SQLiteManager('expenses.db')
        self.init_ui()





    def init_ui(self):
        self.setWindowTitle('Expense Tracker')
        layout = QVBoxLayout()

        # Создание таблицы для отображения данных
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)  # Скрыть названия строк
        self.table.verticalHeader().setMinimumWidth(0)  # Установить минимальную ширину названий строк
        self.table.verticalHeader().setDefaultSectionSize(25)  # Установить фиксированную высоту строк
        layout.addWidget(self.table)



        layout.addWidget(self.daily_table)


        # Создание кнопки для добавления данных
        # Добавляем виджеты для выбора категорий, ввода суммы и кнопки "Add"
        category_combo = QComboBox()
        category_combo.addItems(['Категория 1', 'Категория 2', 'Категория 3'])  # Замените на свои категории
        amount_edit = QLineEdit()
        #add_button = QPushButton('Add')
        #add_button.clicked.connect(self.add_expense_row)

        layout.addWidget(category_combo)
        layout.addWidget(amount_edit)

        add_button = QPushButton('Add Expense')
        add_button.clicked.connect(lambda: self.add_expense_big(category_combo, amount_edit))
        layout.addWidget(add_button)

        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        # Проверяем наличие таблицы 'Expence' и создаем ее, если она отсутствует
        self.sqlite_manager.execute_query("CREATE TABLE IF NOT EXISTS Expence (id INTEGER PRIMARY KEY, date TEXT, amount REAL, category TEXT, comment TEXT)")

        # Получаем данные из таблицы и отображаем их в таблице
        # Получаем данные из таблицы без столбца 'id'
        data = self.sqlite_manager.fetch_data("SELECT date, amount, category, comment FROM Expence")
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
        self.table.itemChanged.connect(self.update_data_in_database)



    def update_data_in_database(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        print(new_value)

        # Получаем значение id из первой ячейки в строке
        id_value = self.table.item(row, col).text()

        column_name = self.table.horizontalHeaderItem(col).text()
        print(column_name)
        query = f"UPDATE Expence SET {column_name} = '{new_value}' WHERE id = {id_value}"
        self.sqlite_manager.execute_query(query)
        print('Donre to aql')

    def add_expense_big (self, category, amount):
        # Добавление новой записи в таблицу
        # Здесь можно добавить диалоговое окно для ввода данных


        self.sqlite_manager.execute_query(f"INSERT INTO Expence (date, amount, category, comment) VALUES ('2024-03-10', '{amount.text()}', '{category.currentText()}', 'Lunch')")

        # Обновление отображаемых данных в таблице
        self.load_data()
    def add_expense(self):
        # Добавление новой записи в таблицу
        # Здесь можно добавить диалоговое окно для ввода данных


        self.sqlite_manager.execute_query(f"INSERT INTO Expence (date, amount, category, comment) VALUES ('2024-03-10', '555', 'Категоия моя ', 'Lunch')")

        # Обновление отображаемых данных в таблице
        self.load_data()


    def calculate_daily_total(self, date):
        query = f"SELECT SUM(amount) FROM Expence WHERE date = '{date}'"
        result = self.sqlite_manager.fetch_data(query)
        return result[0][0] if result[0][0] is not None else 0

    def add_expense_row(self):
        category = self.category_combo.currentText()
        amount = self.amount_edit.text()

        # Добавляем новую строку в таблицу с выбранными данными
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem('Дата'))
        self.table.setItem(row_position, 1, QTableWidgetItem(amount))
        self.table.setItem(row_position, 2, QTableWidgetItem(category))
        self.table.setItem(row_position, 3, QTableWidgetItem('Комментарий'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    expense_app = ExpenseApp()
    expense_app.show()
    sys.exit(app.exec())
