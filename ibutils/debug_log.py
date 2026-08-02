from inspect import stack
from sys import stdout
from pathlib import Path


def debug_log(*args, wait: bool = False):
    print(f"Debug-Log in File {stack()[1].filename}, line {stack()[1].lineno}")
    
    print(*args)
    if wait:
        input("Press 'Enter' to continue")
        stdout.write("\033[F" + "\033[K")

def no_print():
    def print(*args, **kwargs):
        pass
    return print

def log_print(path: str | Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    def print(*args, sep=" ", end="\n"):
        with path.open("a", encoding="utf-8") as file:
            file.write(sep.join(map(str, args)) + end)

    return print