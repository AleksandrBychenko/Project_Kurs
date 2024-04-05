import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import *

from Project_bookkeeper.bookkeeper.models.budget import BudgetTableWidget
from Project_bookkeeper.bookkeeper.models.expense import ExpenseTableWidget
from Project_bookkeeper.bookkeeper.repository.abstract_repository import AbstractRepository
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

from Project_bookkeeper.bookkeeper.models.category import Category, CategoryEditor

import sys
from PySide6.QtWidgets import *

from datetime import datetime

class Bookkeeeper(QWidget):
    def __init__(self):
        super().__init__()
        self.sqlite_manager = SQLiteManager('DatabaseBookkeeper.db')
        self.init_ui()

    def init_ui(self):
        #Название приложения
        self.setWindowTitle('The Bookkeeper App')
        layout = QVBoxLayout()

        self.label = QLabel("Последние расходы")
        layout.addWidget(self.label)

        self.expense_table = ExpenseTableWidget(self.sqlite_manager)
        layout.addWidget(self.expense_table)

        self.label = QLabel("Бюджет")
        layout.addWidget(self.label)

        self.budget_table = BudgetTableWidget(self.sqlite_manager)
        layout.addWidget(self.budget_table)

        self.button = QPushButton("Пересчитать данные")
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

        self.label = QLabel("Настройки:")
        layout.addWidget(self.label)

        repo = AbstractRepository('DatabaseBookkeeper.db')
        self.category_combo = CategoryEditor(repo)
        layout.addWidget(self.category_combo)

        amount_edit = QLineEdit()
        layout.addWidget(amount_edit)
        add_button = QPushButton('Добавить Расходы')
        add_button.clicked.connect(lambda: self.add_expense_big(self.category_combo, amount_edit))
        layout.addWidget(add_button)

        button_layout = QHBoxLayout()
        # Создаем кнопки
        button1 = QPushButton("Убрать последний Расход")
        button2 = QPushButton("Удалить базу данных Расходы")

        button1.clicked.connect(self.Delet_Last)
        button2.clicked.connect(self.Delet_Base)
        # Добавляем кнопки в горизонтальный layout
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Что будет пори изменении клеток в таблицах
        self.expense_table.expense_changes()
        self.budget_table.buget_changes()

    # Функция для кнопки Добавить щначение в базу данных
    def add_expense_big (self, category, amount):
        # Добавление новой записи в таблицу

        self.sqlite_manager.execute_query(f"INSERT INTO expence (date, amount, category, comment) VALUES ('{datetime.now().date()}', '{amount.text()}', '{category.get_selected_category()}', '')")
        # Обновление отображаемых данных в таблице
        # Связываем изменения в ячейках таблицы с обновлением данных в базе данных

        self.expense_table.expense_changes()
        self.budget_table.buget_changes()

    def Delet_Base(self):
        self.sqlite_manager.execute_query("DELETE FROM expence")
        self.expense_table.expense_changes()
        self.budget_table.buget_changes()
    def Delet_Last(self):
        # Получение последней добавленной записи из таблицы expence
        last_expense_id = self.sqlite_manager.fetch_data("SELECT id FROM expence ORDER BY id DESC LIMIT 1")

        if last_expense_id:
            # Удаление записи по идентификатору
            self.sqlite_manager.execute_query(f"DELETE FROM expence WHERE id = {last_expense_id[0][0]}")
            # Обновление отображаемых данных в таблице
            self.expense_table.expense_changes()
            self.budget_table.buget_changes()

    def on_button_clicked(self):
        self.expense_table.expense_changes()
        self.budget_table.buget_changes()


