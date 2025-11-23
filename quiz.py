import os
import pathlib

import yaml
from PySide6.QtCore import QObject, Signal, Property


class Quiz(QObject):

    questionChanged = Signal()

    def __init__(self, file_path: os.PathLike | str | bytes):
        super().__init__()
        self.file_location = pathlib.Path(file_path).parent
        with open(file_path, "r") as f:
            self._data = yaml.safe_load(f)
        self.current_question = self._data[0]

    @Property(str, notify=questionChanged)
    def question(self):
        return self.current_question.get("question", "")

    @Property(str, notify=questionChanged)
    def mainImage(self):
        return str(self.file_location / self.current_question.get("image", ""))

    @Property(list, notify=questionChanged)
    def options(self):
        return self.current_question.get("options", [])
