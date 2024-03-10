#моя реализация

import sqlite3

class SQLiteManager:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

"""
# Создайте экземпляр класса SQLiteManager
sqlite_manager = SQLiteManager('database.db')

# Пример выполнения запроса SELECT
data = sqlite_manager.fetch_data("SELECT * FROM your_table")

# Пример выполнения запроса UPDATE
sqlite_manager.execute_query("UPDATE your_table SET column_name = 'new_value' WHERE condition")

# Закройте соединение с базой данных после использования
sqlite_manager.close_connection()

"""