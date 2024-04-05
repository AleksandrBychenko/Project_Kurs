"""
Модель категории расходов
"""
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов, хранит название в атрибуте name и ссылку (id) на
    родителя (категория, подкатегорией которой является данная) в атрибуте parent.
    У категорий верхнего уровня parent = None
    """
    name: str
    parent: int | None = None
    pk: int = 0

    def get_parent(self,
                   repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Returns
        -------
        Объект класса Category или None
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> Iterator['Category']:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self,
                          repo: AbstractRepository['Category']
                          ) -> Iterator['Category']:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
            cls,
            tree: list[tuple[str, str | None]],
            repo: AbstractRepository['Category']) -> list['Category']:
        """
        Создать дерево категорий из списка пар "потомок-родитель".
        Список должен быть топологически отсортирован, т.е. потомки
        не должны встречаться раньше своего родителя.
        Проверка корректности исходных данных не производится.
        При использовании СУБД с проверкой внешних ключей, будет получена
        ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        со стороны СУБД, результат, возможно, будет корректным, если исходные
        данные корректны за исключением сортировки. Если нет, то нет.
        "Мусор на входе, мусор на выходе".

        Parameters
        ----------
        tree - список пар "потомок-родитель"
        repo - репозиторий для сохранения объектов

        Returns
        -------
        Список созданных объектов Category
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = cls(child, created[parent].pk if parent is not None else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())

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

    def update_category_combo(self):
        self.category_combo.clear()
        all_categories = self.repo.get_all()
        for category in all_categories:
            self.category_combo.addItem(category.name)

    def add_category(self):
        # Здесь должна быть реализация добавления новой категории в репозиторий
        # Например:
        new_category_name = self.amount_edit.text()
        new_category = Category(name=new_category_name)
        self.repo.add(new_category)
        self.update_category_combo()


    def remove_category(self):
        current_category = self.category_combo.currentText()
        # Здесь должна быть реализация удаления категории из репозитория
        #Например:
        self.repo.remove(current_category)
        self.update_category_combo()


#--------------------------

class Category2:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class AbstractRepository2:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        ''')
        self.conn.commit()

    def add(self, category):
        self.cursor.execute('''
            INSERT INTO categories (name, parent_id) VALUES (?, ?)
        ''', (category.name, self.get_parent_id(category.parent)))
        self.conn.commit()

    def remove(self, category_name):
        self.cursor.execute('''
            DELETE FROM categories WHERE name = ?
        ''', (category_name,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute('SELECT name FROM categories')
        return [Category(name) for name, in self.cursor.fetchall()]

    def get_parent_id(self, parent_name):
        if parent_name is None:
            return None
        self.cursor.execute('SELECT id FROM categories WHERE name = ?', (parent_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

# Основной класс редактора категорий
class CategoryEditor2(QWidget):
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