from PyQt6.QtWidgets import (
    QProgressBar,
)

from ibutils.gui.base_window import BaseWindow

_MAX_VALUE = 100


class LoadBar(BaseWindow):

    def __init__(self, title: str | None = "Loading..."):

        if title is None:
            title = "Loading..."

        super().__init__(
            title=title,
            can_maximized=False
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, _MAX_VALUE)
        self.progress_bar.setTextVisible(True)

        self._eta: str | None = None

        self.set_progress(0)

        self.addWidget(self.progress_bar)

    def set_progress(self, value: int) -> int:
        self.progress_bar.setValue(value)
        self._update_format()
        return self.progress_bar.value()

    def add_progress(self, value: int) -> int:
        new_value = self.progress_bar.value() + value
        self.progress_bar.setValue(new_value)
        self._update_format()
        return self.progress_bar.value()

    def set_maximum(self, value: int):
        self.progress_bar.setRange(0, value)
        self._update_format()

    def set_eta(self, value: str | None):
        self._eta = value
        self._update_format()

    def _update_format(self):
        if self._eta is None:
            self.progress_bar.setFormat("%p%")
        else:
            self.progress_bar.setFormat(
                f"%p% [{self._eta}]"
            )

    @property
    def finished(self) -> bool:
        return self.progress_bar.value() >= self.progress_bar.maximum()

    def get_progress(self) -> int:
        return self.progress_bar.value()