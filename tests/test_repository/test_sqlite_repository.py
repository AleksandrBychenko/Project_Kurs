import unittest
import sqlite3
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

class TestSQLiteManager(unittest.TestCase):

    def setUp(self):
        self.sqlite_manager = SQLiteManager(':memory:')  # Используем временную базу данных для тестов

    def tearDown(self):
        self.sqlite_manager.close_connection()

    def test_execute_query(self):
        # Создаем таблицу для тестирования
        self.sqlite_manager.execute_query("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")

        # Проверяем, что таблица создана успешно
        result = self.sqlite_manager.fetch_data("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'")
        self.assertTrue(result)

    def test_fetch_data(self):
        # Вставляем данные для тестирования
        self.sqlite_manager.execute_query("INSERT INTO test_table (name) VALUES ('test_data')")

        # Получаем данные из таблицы
        result = self.sqlite_manager.fetch_data("SELECT * FROM test_table")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'test_data')

"""
if __name__ == '__main__':
    unittest.main()
"""