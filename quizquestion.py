from typing import Optional

from PySide6.QtCore import QObject, Signal, Property, Slot


class QuizQuestion(QObject):
    def __init__(self, data: dict, parent=None):
        super(QuizQuestion, self).__init__(parent)
        self._data = data
        self.selection_index: Optional[int] = None

    def select(self, index: Optional[int] = None):
        self.selection_index = index

    @property
    def selection(self) -> Optional[dict]:
        if self.selection_index is None:
            return None
        try:
            return self._data["options"][self.selection_index]
        except (IndexError, KeyError):
            return None

    @property
    def options(self):
        result = []
        for index, option in enumerate(self._data.get("options", [])):
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

    @property
    def image(self) -> Optional[str]:
        selection = self.selection
        if selection:
            try:
                return selection["image"]
            except KeyError:
                pass
        return self._data.get("image", None)

    @property
    def feedback(self) -> str:
        selection = self.selection
        if selection:
            return selection.get("feedback", "")
        else:
            return ""
