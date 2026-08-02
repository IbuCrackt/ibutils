from multiprocessing import Pipe
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
from enum import Enum, auto

from utils.gui import LoadBar

class Command(Enum):
    SET = auto()
    ADD = auto()
    TITLE = auto()
    MAX_VALUE = auto()
    CLOSE = auto()


def run(conn):
    app = QApplication(sys.argv)

    window = LoadBar()
    window.show()

    window.closed.connect(lambda: conn.close())

    def update():
        while conn.poll():

            command, value = conn.recv()

            match command:

                case Command.SET: 
                    window.set_progress(value)

                case Command.ADD:
                    window.add_progress(value)

                case Command.TITLE:
                    window.setWindowTitle(value)

                case Command.MAX_VALUE:
                    window.set_maximum(value)

                case Command.CLOSE:
                    window.close()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(20)

    app.exec()

    conn.close()