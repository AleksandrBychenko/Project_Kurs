from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class CustomTable(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(['Сумма', 'Бюджет', 'Разница'])

        # Установка параметров таблицы
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_data(self, data):
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]) if data else 0)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.setItem(row_num, col_num, item)

    def set_table_header(self, header_text):
        self.setHorizontalHeaderLabels(header_text)

    def set_row_labels(self, row_labels):
        for row_num, label in enumerate(row_labels):
            item = QTableWidgetItem(label)
            self.setVerticalHeaderItem(row_num, item)