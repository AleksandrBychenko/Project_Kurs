import sqlite3

from Project_bookkeeper.bookkeeper.models.category import Category
class AbstractRepository:
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