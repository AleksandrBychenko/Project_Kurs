"""
Описан класс, представляющий расходную операцию
"""
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class ExpenseTableWidget(QTableWidget):
    def __init__(self, sqlite_manager, parent=None):
        super().__init__(parent)
        self.sqlite_manager = sqlite_manager
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setMinimumWidth(0)
        self.verticalHeader().setDefaultSectionSize(25)
        self.setFixedHeight(150)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def expense_changes(self):
        # Проверяем наличие таблицы 'Expence' и создаем ее, если она отсутствует
        self.sqlite_manager.execute_query("CREATE TABLE IF NOT EXISTS expence (id INTEGER PRIMARY KEY, date TEXT, amount REAL, category TEXT, comment TEXT)")

        data = self.sqlite_manager.fetch_data("SELECT date, amount, category, comment FROM expence")

        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]) if data else 0)

        header_labels = [description[0] for description in self.sqlite_manager.cursor.description]
        self.setHorizontalHeaderLabels(header_labels)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.setItem(row_num, col_num, item)

        # Установка размеров таблицы для заполнения всей доступной высоты окна
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Связываем изменения в ячейках таблицы с обновлением данных в базе данных
        self.itemChanged.connect(self.update_data_in_expence)

    def update_data_in_expence(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        #print(new_value)
        #print(row)

        id_value = row + 1

        column_name = self.horizontalHeaderItem(col).text()
        #print(column_name)
        query = f"UPDATE Expence SET {column_name} = '{new_value}' WHERE id = {id_value}"
        #print(query)

        self.sqlite_manager.execute_query(query)
        #self.buget_changes()
