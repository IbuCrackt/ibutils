_MAX_BAR_WIDTH = 20

from multiprocessing import Pipe, Process

from ._loadbar_process import Command, run


class LoadBar:
    def __init__(self, max_value: int = 100):

        parent, child = Pipe()

        self._conn = parent
        self._process = Process(
            target=run,
            args=(child,),
            daemon=True,
        )
        self._process.start()
        self.set_maximum(max_value)

    def set_progress(self, value):
        self._send(Command.SET, value)

    def add_progress(self, value=1):
        self._send(Command.ADD, value)

    def set_title(self, title: str):
        self._send(Command.TITLE, title)

    def set_maximum(self, value: int):
        self._send(Command.MAX_VALUE, value)

    def close(self):
        if self._process.is_alive():
            self._send(Command.CLOSE)

            self._process.join(timeout=2)

        if self._process.is_alive():
            self._process.terminate()

    def _send(self, command, value=None):
        if not self._process.is_alive():
            return False

        try:
            self._conn.send((command, value))
            return True

        except (BrokenPipeError, EOFError, OSError):
            return False


def print_load_bar(value, max_value):
    bar_width = int((value / max_value) * _MAX_BAR_WIDTH)
    printed_string = "\r[" + "=" * bar_width + " " * (_MAX_BAR_WIDTH - bar_width) + f"] {value} / {max_value}"
    print(printed_string, end="", flush=True)