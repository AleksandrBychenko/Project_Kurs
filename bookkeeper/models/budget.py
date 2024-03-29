from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel
from datetime import datetime

class BudgetTableWidget(QTableWidget):
    def __init__(self, sqlite_manager, parent=None):
        super().__init__(parent)
        self.sqlite_manager = sqlite_manager
        self.initUI()

    def initUI(self):
        '''
        layout = QVBoxLayout(self)
        self.label = QLabel("Бюджет")
        layout.addWidget(self.label)
        '''
        layout = QVBoxLayout(self)
        self.table_widget = QTableWidget(3, 3)  # Создание таблицы 3x3
        # Названия столбцов


        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_widget)

    def buget_changes(self):
        self.sqlite_manager.execute_query(
            "CREATE TABLE IF NOT EXISTS Budget (id INTEGER PRIMARY KEY, column1 TEXT, column2 TEXT, column3 TEXT)")

        row_count = self.sqlite_manager.fetch_data("SELECT COUNT(*) FROM Budget")[0][0]
        # Добавление пустых строк, если их меньше 3
        while row_count < 3:
            self.sqlite_manager.execute_query(
                "INSERT INTO Budget (column1, column2, column3) VALUES ('', '', '')")
            row_count += 1



        self.ostatok()

        data = self.sqlite_manager.fetch_data("SELECT column1, column2, column3 FROM Budget")

        # Установка названий строк и столбцов
        row_headers = ['День', 'Неделя', 'Месяц']
        column_headers = ['Траты', 'Бюджет', 'Остаток']
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

    def ostatok(self):
        # --------------------
        # Получение всех значений из столбца amount в таблице expence
        # fetch_query = "SELECT amount FROM expence"
        # Получение текущего месяца и года
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Получение текущей даты и времени
        now = datetime.now()
        year_now, current_week = now.isocalendar()[:2]
        # Получение номера текущего дня
        current_day = now.day

        print(current_month)
        print(current_year)
        print(current_week)
        print(current_day)
        # Получение всех значений из столбца amount в таблице expence за текущий месяц и год
        fetch_query = f"""
                    SELECT amount FROM expence
                    WHERE strftime('%m', date) = '{current_month:02d}'
                    AND strftime('%Y', date) = '{current_year}'
                """
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
        update_query = f"UPDATE Budget SET column1 = {total_sum} WHERE id = 3"
        self.sqlite_manager.execute_query(update_query)

        # -----------

        # Получение всех значений из столбца amount в таблице expence за текущий месяц и год
        fetch_query = f"""
                    SELECT amount FROM expence
                    WHERE strftime('%d', date) = '{current_day}'
                    AND strftime('%Y', date) = '{current_year}'
                """
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
        update_query = f"UPDATE Budget SET column1 = {total_sum} WHERE id = 1"
        self.sqlite_manager.execute_query(update_query)
        # -----------
        # -----------

        # Получение всех значений из столбца amount в таблице expence за текущий месяц и год
        fetch_query = f"""
                    SELECT amount FROM expence
                    WHERE strftime('%W', date) = '{current_week}'
                    AND strftime('%Y', date) = '{current_year}'
                """
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

        # -----------
        # Обновляем первый столбец в таблице Budget, где id = 2, значением суммы
        for i in range(3):
            try:
                update_query = f"UPDATE Budget SET column3 = column2 - column1  WHERE id = {i + 1}"
                self.sqlite_manager.execute_query(update_query)
            except ValueError:
                # Если не удалось преобразовать в число, пропускаем это значение
                continue

    def update_data_in_budget(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text()
        print(new_value)
        print(row)

        id_value = row + 1

        column_name = self.table_widget.horizontalHeaderItem(col).text()
        print(column_name)
        if column_name == 'Траты':
            column_name = 'column1'
        if column_name == 'Бюджет':
            column_name = 'column2'
        if column_name == 'Остаток':
            column_name = 'column3'
        query = f"UPDATE Budget SET {column_name} = '{new_value}' WHERE id = {id_value}"
        print(query)

        self.sqlite_manager.execute_query(query)

