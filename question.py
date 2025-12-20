import pathlib
from collections import OrderedDict
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QImage

from answer import Answer
from plot import Plot


class Question(QObject):
    def __init__(self, data: dict, file_location: pathlib.Path):
        super(Question, self).__init__(parent=None)
        self.file_location = file_location
        self.question = data.get("question", "")
        if "image" in data:
            self.image_url = data["image"]
            self._image = QImage(str(file_location / self.image_url))
        elif "plot" in data:
            self.plot = Plot(data["plot"])
            self._image = self.plot.make_image()
        else:
            self._image = None
        self.answers = [Answer(d, self.file_location) for d in data.get("options", [])]
        self.selection = None

    def get_data_dict(self):
        result = dict()
        result["question"] = self.question
        if hasattr(self, "image_url"):
            result["image"] = self.image_url
        elif hasattr(self, "plot"):
            result["plot"] = self.plot.get_data_dict()
        result["options"] = [answer.get_data_dict() for answer in self.answers]
        return result

    def select(self, index: Optional[int] = None):
        try:
            self.selection = self.answers[index]
        except (IndexError, KeyError):
            self.selection = None

    @property
    def correct(self) -> bool:
        if self.selection is None:
            return False
        else:
            return self.selection.correct

    @property
    def options(self):
        result = []
        for index, answer in enumerate(self.answers):
            selected = answer is self.selection
            result.append(
                {
                    "index": index,
                    "answer": answer.text,
                    "selected": selected,
                }
            )
        return result

    @property
    def image(self) -> Optional[QImage]:
        result = None
        if self.selection is not None:
            result = self.selection.image
        return result or self._image

    @property
    def feedback(self) -> str:
        if self.selection is not None:
            return self.selection.feedback
        else:
            return ""
