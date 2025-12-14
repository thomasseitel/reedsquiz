import sys
import pathlib
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from quiz import Quiz

if __name__ == "__main__":
    BASE_DIR = pathlib.Path(__file__).parent

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    quiz = Quiz(BASE_DIR / "example" / "example.yaml")
    engine.rootContext().setContextProperty("quiz", quiz)
    engine.addImageProvider("imageprovider", quiz.image_provider)
    engine.load(BASE_DIR / "main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    app.aboutToQuit.connect(engine.deleteLater)
    sys.exit(app.exec())
