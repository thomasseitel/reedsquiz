import pathlib

from PySide6.QtCore import QObject
from PySide6.QtGui import QImage


class Answer(QObject):
    def __init__(self, data: dict, file_location: pathlib.Path):
        super(Answer, self).__init__()
        self.text = data.get("answer")
        self.correct = data.get("correct", False)
        self.feedback = data.get("feedback", "")
        self.image_url = data.get("image", "")
        if self.image_url:
            self.image = QImage(str(file_location / self.image_url))
        else:
            self.image = None
