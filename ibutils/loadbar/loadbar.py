_MAX_BAR_WIDTH = 20
_TIME_ESTIMATION_VALUES = 0.1

import time
from collections import deque
from multiprocessing import Pipe, Process

from ._loadbar_process import Command, run


class LoadBar:
    def __init__(
        self,
        max_value: int = 100,
        auto_time_estimation: bool = False,
    ):
        parent, child = Pipe()

        self._conn = parent
        self._process = Process(
            target=run,
            args=(child,),
            daemon=True,
        )
        self._process.start()

        self._time_estimation = auto_time_estimation
        self._title = ""
        self._progress_history = deque()

        self.set_maximum(max_value)

    def set_progress(self, value):
        self._record_progress(value)
        self._send_progress(value)

    def add_progress(self, value=1):
        if not self._progress_history:
            current_value = 0
        else:
            current_value = self._progress_history[-1][0]
        self.set_progress(current_value + value)

    def set_title(self, title: str):
        self._title = title
        self._send(Command.TITLE, title)

    def set_maximum(self, value: int):
        self._max_value = value
        self._send(Command.MAX_VALUE, value)

    def close(self):
        if self._process.is_alive():
            self._send(Command.CLOSE)

            self._process.join(timeout=2)

        if self._process.is_alive():
            self._process.terminate()

    def set_time_estimation(self, value: str):
        self._send(Command.ETA, value)

    def _record_progress(self, value: int):
        if not self._time_estimation:
            return

        now = time.monotonic()
        self._progress_history.append((value, now))

        window = max(
            1,
            int(self._max_value * _TIME_ESTIMATION_VALUES)
        )

        if value <= window:
            return

        while (
            len(self._progress_history) > 1
            and value - self._progress_history[0][0] > window
        ):
            self._progress_history.popleft()

    def _get_time_estimation(self):
        if not self._time_estimation:
            return None
        
        if len(self._progress_history) < 2:
            return None

        old_value, old_time = self._progress_history[0]
        current_value, current_time = self._progress_history[-1]

        print(old_value, old_time)
        print(current_value, current_time)

        progress = current_value - old_value
        elapsed = current_time - old_time

        if progress <= 0 or elapsed <= 0:
            return None
        steps_per_second = progress / elapsed
        remaining_steps = self._max_value - current_value

        return remaining_steps / steps_per_second

    def _send_progress(self, value):
        eta = self._get_time_estimation()

        if eta is not None:
            self._send(Command.ETA, _format_time(eta))
        self._send(Command.SET, value)

    def _send(self, command, value=None):
        if not self._process.is_alive():
            return False
        try:
            self._conn.send((command, value))
            return True
        except (BrokenPipeError, EOFError, OSError):
            return False


def _format_time(seconds: float) -> str:
    """Formats seconds into a human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {seconds}s"

    hours = minutes // 60
    minutes %= 60

    return f"{hours}h {minutes}m"


def print_load_bar(value, max_value):
    bar_width = int((value / max_value) * _MAX_BAR_WIDTH)

    printed_string = (
        "\r["
        + "=" * bar_width
        + " " * (_MAX_BAR_WIDTH - bar_width)
        + f"] {value} / {max_value}"
    )

    print(printed_string, end="", flush=True)