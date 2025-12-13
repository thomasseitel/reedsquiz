from typing import Optional

from PySide6.QtGui import QImage, QColor
from PySide6.QtQuick import QQuickImageProvider

from quizquestion import QuizQuestion


class QuizImageHandler(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._image_data = None
        self.placeholder = QImage(100, 100, QImage.Format.Format_RGB32)
        self.placeholder.fill(QColor("red"))
        self.question: Optional[QuizQuestion] = None

    def set_question(self, question: QuizQuestion):
        self.question = question

    def requestImage(self, id, size, requestedSize):
        image = None
        if self.question:
            image = self.question.image
        if image is None:
            return self.placeholder
        else:
            return image
