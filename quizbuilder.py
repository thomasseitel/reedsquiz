import sys

from PySide6.QtWidgets import QMainWindow, QApplication


class QuizBuilder(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


if __name__ == "__main__":
    app = QApplication()
    mainwindow = QuizBuilder()
    mainwindow.show()
    sys.exit(app.exec_())
