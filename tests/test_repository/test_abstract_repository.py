import sqlite3
import pytest
from Project_bookkeeper.bookkeeper.models.category import Category
from Project_bookkeeper.bookkeeper.repository.abstract_repository import AbstractRepository

@pytest.fixture
def db_path():
    return 'test.db'

def test_create_table(db_path):
    repository = AbstractRepository(db_path)
    repository.conn.execute("DROP TABLE IF EXISTS categories")
    repository.create_table()
    repository.conn.execute("INSERT INTO categories (name, parent_id) VALUES ('Test', NULL)")
    data = repository.get_all()
    assert len(data) == 1
    assert data[0].name == 'Test'
    repository.conn.close()

def test_add(db_path):
    repository = AbstractRepository(db_path)
    repository.create_table()
    category = Category('Test')
    repository.add(category)
    data = repository.get_all()
    assert len(data) == 1
    assert data[0].name == 'Test'
    repository.conn.close()

def test_remove(db_path):
    repository = AbstractRepository(db_path)
    repository.create_table()
    repository.add(Category('Test'))
    repository.remove('Test')
    data = repository.get_all()
    assert len(data) == 0
    repository.conn.close()

def test_get_all(db_path):
    repository = AbstractRepository(db_path)
    repository.create_table()
    repository.add(Category('Test1'))
    repository.add(Category('Test2'))
    data = repository.get_all()
    assert len(data) == 2
    assert data[0].name == 'Test1'
    assert data[1].name == 'Test2'
    repository.conn.close()



if __name__ == '__main__':
    pytest.main()