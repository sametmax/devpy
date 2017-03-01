import tempfile

from pathlib import Path


def temp_dir(name, root=None):
    root = root or tempfile.gettempdir()
    directory = Path(root) / name
    directory.mkdir(exist_ok=True)
    return directory
