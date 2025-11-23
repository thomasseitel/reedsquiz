import os
import pathlib

import yaml
from PySide6.QtCore import QObject, Signal, Property, Slot


class Quiz(QObject):

    questionChanged = Signal()

    def __init__(self, file_path: os.PathLike | str | bytes):
        super().__init__()
        self.file_location = pathlib.Path(file_path).parent
        with open(file_path, "r") as f:
            self._data = yaml.safe_load(f)
        self.questionIndex = None
        self.current_selection = None
        self.loadNextQuestion()

    def loadNextQuestion(self):
        if self.questionIndex is None:
            self.questionIndex = 0
        else:
            self.questionIndex += 1
        self.current_selection = None
        self.questionChanged.emit()

    @property
    def current_question(self):
        return self._data[self.questionIndex]

    @Slot(int)
    def submitAnswer(self, index: int):
        self.current_selection = index
        self.questionChanged.emit()

    @Property(str, notify=questionChanged)
    def question(self):
        return self.current_question.get("question", "")

    @Property(str, notify=questionChanged)
    def mainImage(self):
        question = self.current_question
        if self.current_selection is not None:
            selected_option = question["options"][self.current_selection]
            image = selected_option.get("image", "")
            if image:
                return str(self.file_location / image)
        return str(self.file_location / self.current_question.get("image", ""))

    @Property(list, notify=questionChanged)
    def options(self):
        option_data = self.current_question.get("options", [])
        results = []
        for index, option in enumerate(option_data):
            selected = index == self.current_selection
            results.append(
                {
                    "index": index,
                    "answer": option.get("answer", ""),
                    "feedback": (option.get("feedback", "") if selected else ""),
                    "selected": selected,
                }
            )
        return results
