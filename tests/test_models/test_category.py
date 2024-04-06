import pytest

from Project_bookkeeper.bookkeeper.models.category import Category, CategoryEditor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox
from unittest.mock import MagicMock

class TestCategory:
    def test_category_initialization(self):
        category = Category('Test', 'Parent')
        assert category.name == 'Test'
        assert category.parent == 'Parent'

class TestCategoryEditor:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    def test_initUI(self, mock_repo):
        app = QApplication([])
        editor = CategoryEditor(mock_repo)
        assert isinstance(editor.layout, QVBoxLayout)
        assert isinstance(editor.category_combo, QComboBox)
        assert isinstance(editor.amount_edit, QLineEdit)
        assert isinstance(editor.add_button, QPushButton)
        assert isinstance(editor.remove_button, QPushButton)

    def test_get_selected_category(self, mock_repo):
        #app = QApplication([])
        editor = CategoryEditor(mock_repo)
        editor.category_combo.addItem('Test')
        editor.category_combo.setCurrentIndex(0)
        assert editor.get_selected_category() == 'Test'

    def test_update_category_combo(self, mock_repo):
        #app = QApplication([])
        editor = CategoryEditor(mock_repo)
        mock_repo.get_all.return_value = [Category('Test1'), Category('Test2')]
        editor.update_category_combo()
        assert editor.category_combo.count() == 2
        assert editor.category_combo.itemText(0) == 'Test1'
        assert editor.category_combo.itemText(1) == 'Test2'

if __name__ == '__main__':
    pytest.main()