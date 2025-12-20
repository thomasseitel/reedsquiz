import os
import pathlib

import yaml
from PySide6.QtCore import QObject, Signal, Property, Slot

from quizimagehandler import QuizImageHandler
from question import Question


class Quiz(QObject):

    questionChanged = Signal()
    quizFinished = Signal()

    def __init__(self, file_path: os.PathLike | str | bytes):
        super().__init__()
        file_location = pathlib.Path(file_path).parent
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            self.questions = [Question(d, file_location) for d in data]
        self.image_provider = QuizImageHandler()
        self.questionIndex = None
        self.nextQuestion()

    def to_yaml(self) -> str:
        data = [question.get_data_dict() for question in self.questions]
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

    def save_as(self, file_path: os.PathLike | str | bytes):
        with open(file_path, "w") as f:
            f.write(self.to_yaml())

    @Slot()
    def nextQuestion(self):
        if self.questionIndex is None:
            self.questionIndex = 0
        else:
            self.questionIndex += 1
        if self.questionIndex >= len(self.questions):
            self.quizFinished.emit()
        else:
            self.image_provider.set_question(self.current_question)
            self.questionChanged.emit()

    @property
    def current_question(self) -> Question:
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

    @Property(bool, notify=questionChanged)
    def mayContinue(self):
        return self.current_question.correct

    @Property(str, notify=questionChanged)
    def continueText(self):
        if self.questionIndex < len(self.questions) - 1:
            return "Next"
        else:
            return "Finished"
