import os
import pathlib

import yaml
from PySide6.QtCore import QObject, Signal, Property, Slot

from quizimagehandler import QuizImageHandler
from quizquestion import QuizQuestion


class Quiz(QObject):

    questionChanged = Signal()

    def __init__(self, file_path: os.PathLike | str | bytes):
        super().__init__()
        file_location = pathlib.Path(file_path).parent
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            self.questions = [QuizQuestion(d, file_location) for d in data]
        self.image_provider = QuizImageHandler()
        self.questionIndex = None
        self.loadNextQuestion()

    def loadNextQuestion(self):
        if self.questionIndex is None:
            self.questionIndex = 0
        else:
            self.questionIndex += 1
        self.image_provider.set_question(self.current_question)
        self.questionChanged.emit()

    @property
    def current_question(self) -> QuizQuestion:
        return self.questions[self.questionIndex]

    @Slot(int)
    def submitAnswer(self, index: int):
        self.current_question.select(index)
        self.questionChanged.emit()

    @Property(str, notify=questionChanged)
    def question(self):
        return self.current_question.question

    @Property(list, notify=questionChanged)
    def options(self):
        return self.current_question.options

    @Property(str, notify=questionChanged)
    def feedback(self):
        return self.current_question.feedback
