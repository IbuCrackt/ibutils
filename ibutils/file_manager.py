import json
import os
from inspect import stack
from pathlib import Path


class FileManager:
    """Ibu's eigener FileManager mit einfachen Funktionen um Dateien logisch zu managen.
    """
    @classmethod
    def get_current_path(cls, file_path: str | Path | None = None, stack_i: int = 1):
        """Gibt den derzeitigen Pfad zum i-ten ausführendem File aus.
        """
        path = Path(stack()[stack_i].filename).resolve()
        if file_path:
            return path.parent.joinpath(file_path)
        return path

    @classmethod
    def load_json(cls, file_path: str | Path) -> dict:
        """Lädt ein Json-File aus file_path abhängig von dem ausführendem File.
        """
        path = cls.get_current_path(
            file_path = file_path, 
            stack_i = 2
        )
        with open(os.path.join(path, file_path), 'r') as loaded_file:
            read_file = json.load(loaded_file)
        
        return read_file
    
    @classmethod
    def append_file(cls, file_path, *args):
        """Fügt *args an das Ende vom File file_path hinzu.
        """
        path = cls.get_current_path(
            file_path = file_path,
            stack_i = 2
        )
        with open(os.path.join(path, file_path), 'a') as loaded_file:
            for arg in args:
                loaded_file.write(arg+'\n')