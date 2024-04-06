import sys
from PySide6.QtWidgets import QApplication
from Project_bookkeeper.bookkeeper.view.Bookkeeper import Bookkeeeper

if __name__ == '__main__':
    app = QApplication(sys.argv)
    expense_app = Bookkeeeper()
    expense_app.show()

    sys.exit(app.exec())