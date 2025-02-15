from pathlib import Path
from typing import Optional

import tomllib

from ecologits import __version__


def test_version_alignment():
    poetry_version = get_poetry_version()
    assert __version__ == poetry_version


def get_poetry_version() -> Optional[str]:
    path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
    with open(str(path), "rb") as fd:
        pyproject = tomllib.load(fd)
        return pyproject['project']['version']
