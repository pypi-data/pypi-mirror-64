from pathlib import Path
from dataclasses import dataclass

from boo.errors import DirectoryNotFound, NoRawFileError, NoProcessedFileError
from boo.helper import as_mb


def default_data_folder() -> Path:
    home = Path.home() / ".boo"
    home.mkdir(exist_ok=True)
    return home


def get_folder(directory=None) -> Path:
    if directory is None:
        return default_data_folder()
    elif Path(directory).is_dir():
        return Path(directory)
    else:
        raise DirectoryNotFound(directory)


def file(year, tag="", directory=None):
    return get_folder(directory) / f"{tag}{year}.csv"


class File:
    def __init__(self, year, tag, directory):
        self.path = file(year, tag, directory)
        self.year = year

    def size(self):
        return self.path.stat().st_size

    def mb(self):
        return as_mb(self.size())

    def exists(self):
        return self.path.exists()

    def folder(self):
        return str(self.path.parent)

    def __str__(self):
        try:
            return f"{self.path} ({self.mb()}M)"
        except FileNotFoundError:
            return f"{self.path} (does not exist)"

    def __repr__(self):
        return repr(self.path)

    def print_error(self):
        try:
            self.assert_exists()
        except FileNotFoundError as e:
            print(e)


class Raw(File):
    def __init__(self, year, directory):
        super().__init__(year, "raw", directory)

    def content(self):
        return self.path.read_text(encoding="cp1251")

    def assert_exists(self):
        if not self.exists():
            raise NoRawFileError(self.year)


class Processed(File):
    def __init__(self, year, directory):
        super().__init__(year, "", directory)

    def content(self):
        return self.path.read_text(encoding="utf-8")

    def assert_exists(self):
        if not self.exists():
            raise NoProcessedFileError(self.year)


@dataclass
class Files:
    raw: Raw
    processed: Processed


def locate(year, directory=None):
    return Files(raw=Raw(year, directory), processed=Processed(year, directory))
