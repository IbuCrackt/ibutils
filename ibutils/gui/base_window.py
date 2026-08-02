"""Frameless base window with a custom title bar and edge-resize support."""

from PyQt6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QWidget,
)
from PyQt6.QtCore import (
    Qt, 
    QEvent,
    pyqtSignal,
)
from typing import (
    Callable,
    Literal
)


class BaseWindow(QMainWindow):
    """Base class for all top-level windows in the app.

    Provides a frameless window with an optional custom :class:`TitleBar`,
    manual edge/corner resizing, and thin ``addWidget``/``setColumnStretch``/
    ``setRowStretch`` helpers that forward to the content layout.
    """


    closed = pyqtSignal()
    minimized = pyqtSignal()
    maximized = pyqtSignal()

    def __init__(
        self,
        title: str | None = None,
        can_maximized: bool = True,
        parent=None,
    ):
        super().__init__()

        self.resize_margin = 8
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._parent_window = parent

        # parent handling
        if parent is not None:
            parent.destroyed.connect(self.close)

        # central layout
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.grid = QGridLayout(self.central)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # content widget
        self.content = QWidget()
        self.content_layout = QGridLayout(self.content)

        # titlebar
        self.titlebar_widget = None

        if title is not None:
            from .title_bar_widget import TitleBar

            self.titlebar_widget = TitleBar(
                title,
                self,
                can_maximized
            )

            self._connect_titlebar()

            self.grid.addWidget(self.titlebar_widget, 0, 0)

            self.grid.addWidget(self.content, 1, 0)

            self.grid.setRowStretch(0, 0)
            self.grid.setRowStretch(1, 1)

        else:
            self.grid.addWidget(self.content, 0, 0)

        self.setMouseTracking(True)
        self.installEventFilter(self)

    # titlebar connections
    def _connect_titlebar(self):
        if self.titlebar_widget is not None:
            tb = self.titlebar_widget

            tb.close_button.clicked.connect(self.close_window)
            tb.minimize_button.clicked.connect(self.minimize)

            if hasattr(tb, "maximize_button"):
                tb.maximize_button.clicked.connect(
                    self.maximize
                )

    def close_window(self):
        self.closed.emit()
        self.close()

    def minimize(self):
        self.minimized.emit()
        self.showMinimized()

    def maximize(self):
        self.maximized.emit()
        self.toggle_max_restore()

    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()

            if self.titlebar_widget:
                self.titlebar_widget.maximize_button.setText("□")
        else:
            self.showMaximized()

            if self.titlebar_widget:
                self.titlebar_widget.maximize_button.setText("❐")

    # resize logic
    def eventFilter(self, obj, event):
        if self.isMaximized():
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Type.MouseMove:
            pos = event.position().toPoint()

            edge = self.get_edge(pos)
            self.update_cursor(edge)

        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                pos = event.position().toPoint()

                edge = self.get_edge(pos)

                if edge is not None and self.windowHandle():
                    self.windowHandle().startSystemResize(edge)
                    return True

        return super().eventFilter(obj, event)

    # edge detection
    def get_edge(self, pos):
        rect = self.rect()
        margin = self.resize_margin

        x = pos.x()
        y = pos.y()

        left = x <= margin
        right = x >= rect.width() - margin
        top = y <= margin
        bottom = y >= rect.height() - margin

        if top and left:
            return Qt.Edge.TopEdge | Qt.Edge.LeftEdge
        if top and right:
            return Qt.Edge.TopEdge | Qt.Edge.RightEdge
        if bottom and left:
            return Qt.Edge.BottomEdge | Qt.Edge.LeftEdge
        if bottom and right:
            return Qt.Edge.BottomEdge | Qt.Edge.RightEdge

        if left:
            return Qt.Edge.LeftEdge
        if right:
            return Qt.Edge.RightEdge
        if top:
            return Qt.Edge.TopEdge
        if bottom:
            return Qt.Edge.BottomEdge

        return None

    def update_cursor(self, edge):
        if edge in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
            self.setCursor(Qt.CursorShape.SizeHorCursor)

        elif edge in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
            self.setCursor(Qt.CursorShape.SizeVerCursor)

        elif edge == (Qt.Edge.TopEdge | Qt.Edge.LeftEdge):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)

        elif edge == (Qt.Edge.BottomEdge | Qt.Edge.RightEdge):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)

        elif edge == (Qt.Edge.TopEdge | Qt.Edge.RightEdge):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)

        elif edge == (Qt.Edge.BottomEdge | Qt.Edge.LeftEdge):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)

        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def addWidget(self, *args, **kwargs):
        self.content_layout.addWidget(*args, **kwargs)

    def setColumnStretch(self, *args, **kwargs):
        self.content_layout.setColumnStretch(*args, **kwargs)

    def setRowStretch(self, *args, **kwargs):
        self.content_layout.setRowStretch(*args, **kwargs)

    def reload(self):
        pass
