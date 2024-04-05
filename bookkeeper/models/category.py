"""
Модель категории расходов дял проекта
"""
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox

class Category:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent


# Основной класс редактора категорий
class CategoryEditor(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.category_combo = QComboBox()
        self.update_category_combo()

        self.amount_edit = QLineEdit()

        self.add_button = QPushButton("Добавить категорию")
        self.add_button.clicked.connect(self.add_category)

        self.remove_button = QPushButton("Удалить категорию")
        self.remove_button.clicked.connect(self.remove_category)

        self.layout.addWidget(self.category_combo)
        self.layout.addWidget(self.amount_edit)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

    def get_selected_category(self):
        # Получаем текст выбранной категории
        selected_category = self.category_combo.currentText()
        return selected_category
    def update_category_combo(self):
        self.category_combo.clear()
        all_categories = self.repo.get_all()
        for category in all_categories:
            self.category_combo.addItem(category.name)

    def add_category(self):
        new_category_name = self.amount_edit.text()
        if not new_category_name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории.")
            return
        new_category = Category(new_category_name)
        self.repo.add(new_category)
        self.update_category_combo()
        self.amount_edit.clear()

    def remove_category(self):
        current_category = self.category_combo.currentText()
        if not current_category:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления.")
            return
        self.repo.remove(current_category)
        self.update_category_combo()