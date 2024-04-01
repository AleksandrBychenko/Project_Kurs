import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import *

from Project_bookkeeper.bookkeeper.models.budget import BudgetTableWidget
from Project_bookkeeper.bookkeeper.models.expense import ExpenseTableWidget
from Project_bookkeeper.bookkeeper.repository.abstract_repository import AbstractRepository
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

from Project_bookkeeper.bookkeeper.models.category import Category

import sys
from PySide6.QtWidgets import *

from datetime import datetime

class Bookkeeeper(QWidget):
    def __init__(self):
        super().__init__()
        self.sqlite_manager = SQLiteManager('expence3.db')
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

        # Добавляем котегории
        repo = AbstractRepository[Category]()
        # Создаем дерево категорий
        tree = [
            ('Тип расхода', None),
            ('Прочее', None),
            ('Ежемесячные траты', None),
            ('Еда', None),
            ('Напитки', None),
            ('Еда -> Овощи', 'Еда'),
            ('Еда -> Фрукты', 'Еда'),
            ('Напитки -> Холодные напитки', 'Напитки'),
            ('Напитки -> Горячие напитки', 'Напитки'),
            ('Одежда', None),
            ('Медицина', None),
            ('Непредвиденные расходы', None),

        ]


        category_combo = QComboBox()
        # Получаем все категории из репозитория
        all_categories = repo.get_all()
        # Заполняем QComboBox названиями категорий
        for category in all_categories:
            category_combo.addItem(category.name)
        #category_combo.addItems(['Категория 1', 'Категория 2', 'Категория 3'])  # Замените на свои категории
        amount_edit = QLineEdit()
        layout.addWidget(category_combo)
        layout.addWidget(amount_edit)

        #Добавление кнопок для настройки
        add_button = QPushButton('Добавить Расходы')
        add_button.clicked.connect(lambda: self.add_expense_big(category_combo, amount_edit))
        layout.addWidget(add_button)

        # Создаем горизонтальный layout для кнопок
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

        self.sqlite_manager.execute_query(f"INSERT INTO expence (date, amount, category, comment) VALUES ('{datetime.now().date()}', '{amount.text()}', '{category.currentText()}', '')")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    expense_app = Bookkeeeper()
    expense_app.show()

    sys.exit(app.exec())
