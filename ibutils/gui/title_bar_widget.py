"""Custom, frameless title bar used by :class:`BaseWindow`."""

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .base_window import BaseWindow

class TitleBar(QWidget):
    """Draggable title bar with minimize/maximize/close buttons and an
    extensible left-hand button area (see :meth:`addButton`).
    """

    def __init__(
        self,
        title: str,
        parent: "BaseWindow",
        can_maximized: bool = True
    ):
        super().__init__(parent)

        self._parent_window = parent

        self.can_maximized = can_maximized
        self.setFixedHeight(40)

        self.main_layout = QHBoxLayout(self)

        self.main_layout.setContentsMargins(8, 0, 8, 0)
        self.main_layout.setSpacing(6)

        self.left_layout = QHBoxLayout()
        self.left_layout.setSpacing(6)

        self.center_layout = QHBoxLayout()

        self.title_label = QLabel(title)

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.center_layout.addWidget(self.title_label)

        self.right_layout = QHBoxLayout()
        self.right_layout.setSpacing(6)

        self.minimize_button = QPushButton("_")
        self.minimize_button.setFixedSize(30, 28)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(30, 28)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 28)

        self.right_layout.addWidget(self.minimize_button)

        if can_maximized:
            self.right_layout.addWidget(self.maximize_button)

        self.right_layout.addWidget(self.close_button)

        self.main_layout.addLayout(self.left_layout)

        self.main_layout.addStretch()

        self.main_layout.addLayout(self.center_layout)

        self.main_layout.addStretch()

        self.main_layout.addLayout(self.right_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._parent_window.windowHandle():
                self._parent_window.windowHandle().startSystemMove()

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if not self.can_maximized:
            return
        if (
            event.button() == Qt.MouseButton.LeftButton
            and hasattr(self._parent_window, "toggle_max_restore")
        ):
            self._parent_window.toggle_max_restore()

        super().mouseDoubleClickEvent(event)

    def addButton(
        self,
        text: str,
        width: int = 30,
        callback=None
    ) -> QPushButton:

        button = QPushButton(text)

        button.setFixedSize(width, 28)

        if callback is not None:
            button.clicked.connect(callback)

        self.left_layout.addWidget(button)

        return button
