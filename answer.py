import pathlib
from collections import OrderedDict

from PySide6.QtCore import QObject
from PySide6.QtGui import QImage

from plot import Plot


class Answer(QObject):
    def __init__(self, data: dict, file_location: pathlib.Path):
        super(Answer, self).__init__()
        self.text = data.get("answer")
        self.correct = data.get("correct", False)
        self.feedback = data.get("feedback", "")
        if "image" in data:
            self.image_url = data["image"]
            self.image = QImage(str(file_location / self.image_url))
        elif "plot" in data:
            self.plot = Plot(data["plot"])
            self.image = self.plot.make_image()
        else:
            self.image = None

    def get_data_dict(self):
        result = dict()
        result["answer"] = self.text
        if self.feedback:
            result["feedback"] = self.feedback
        if hasattr(self, "image_url"):
            result["image"] = self.image_url
        elif hasattr(self, "plot"):
            result["plot"] = self.plot.get_data_dict()
        if self.correct:
            result["correct"] = True

        return result
