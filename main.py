import sys
import pathlib
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    BASE_DIR = pathlib.Path(__file__).parent

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(BASE_DIR / "main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
