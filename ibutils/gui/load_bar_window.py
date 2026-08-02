from PyQt6.QtWidgets import (
    QProgressBar,
)

from utils.gui.base_window import BaseWindow

_MAX_VALUE = 100

class LoadBar(BaseWindow):

    def __init__(self, title: str | None = "Loading..."):

        if title is None:
            title = "Loading..."

        super().__init__(
            title = title,
            can_maximized = False
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, _MAX_VALUE)
        self.progress_bar.setTextVisible(True)

        self.addWidget(self.progress_bar)

    def set_progress(self, value: int) -> int:
        self.progress_bar.setValue(value)
        return self.progress_bar.value()

    def add_progress(self, value: int) -> int:
        new_value = self.progress_bar.value() + value
        self.progress_bar.setValue(new_value)
        return self.progress_bar.value()

    def set_maximum(self, value: int):
        self.progress_bar.setRange(0, value)

    @property
    def finished(self) -> bool:
        return self.progress_bar.value() >= _MAX_VALUE

    def get_progress(self) -> int:
        return self.progress_bar.value()