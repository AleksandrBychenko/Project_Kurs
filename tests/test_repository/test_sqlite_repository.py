import pytest
import sqlite3
from Project_bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteManager

#test

@pytest.fixture
def database_name():
    return 'test.db'

def test_execute_query(database_name):
    manager = SQLiteManager(database_name)
    manager.execute_query('CREATE TABLE test (id INTEGER, name TEXT)')
    data = manager.fetch_data('SELECT name FROM test')
    assert len(data) == 0
    manager.close_connection()

def test_fetch_data(database_name):
    manager = SQLiteManager(database_name)
    manager.execute_query("INSERT INTO test VALUES (1, 'Alice')")
    data = manager.fetch_data('SELECT name FROM test')
    assert len(data) == 1
    assert data[0][0] == 'Alice'
    manager.close_connection()

def test_close_connection(database_name):
    manager = SQLiteManager(database_name)
    manager.close_connection()
    with pytest.raises(sqlite3.ProgrammingError):
        manager.execute_query('SELECT 1')

def test_commit(database_name):
    manager = SQLiteManager(database_name)
    manager.execute_query('CREATE TABLE test_commit (id INTEGER, name TEXT)')
    manager.execute_query("INSERT INTO test_commit VALUES (1, 'Bob')")
    data = manager.fetch_data('SELECT name FROM test_commit')
    assert len(data) == 1
    assert data[0][0] == 'Bob'
    manager.commit()
    data_after_commit = manager.fetch_data('SELECT name FROM test_commit')
    assert len(data_after_commit) == 1
    assert data_after_commit[0][0] == 'Bob'
    manager.close_connection()


if __name__ == '__main__':
    pytest.main()