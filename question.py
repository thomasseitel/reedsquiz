import pathlib
from functools import cached_property
from typing import Optional

from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtGui import QImage


class Question(QObject):
    def __init__(self, data: dict, file_location: pathlib.Path):
        super(Question, self).__init__(parent=None)
        self.file_location = file_location
        self._data = data
        self._options = self._data.get("options", [])
        self.selection_index: Optional[int] = None

    def select(self, index: Optional[int] = None):
        self.selection_index = index
        try:
            del self.image
        except AttributeError:
            pass

    @property
    def selection(self) -> Optional[dict]:
        if self.selection_index is None:
            return None
        try:
            return self._data["options"][self.selection_index]
        except (IndexError, KeyError):
            return None

    @property
    def correct(self) -> bool:
        try:
            return self._options[self.selection_index].get("correct", False)
        except (IndexError, KeyError, TypeError):
            return False

    @property
    def options(self):
        result = []
        for index, option in enumerate(self._options):
            selected = index == self.selection_index
            result.append(
                {
                    "index": index,
                    "answer": option.get("answer", ""),
                    "selected": selected,
                }
            )
        return result

    @property
    def question(self) -> str:
        return self._data.get("question", "Question not found")

    @cached_property
    def image(self) -> Optional[QImage]:
        selection = self.selection
        filename = None
        if selection:
            try:
                filename = selection["image"]
            except KeyError:
                pass
        if filename is None:
            filename = self._data.get("image", None)
        if filename is None:
            return None
        else:
            return QImage(str(self.file_location / filename))

    @property
    def feedback(self) -> str:
        selection = self.selection
        if selection:
            return selection.get("feedback", "")
        else:
            return ""
