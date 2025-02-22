from pathlib import Path
from typing import Optional

from ecologits import __version__
from ecologits.utils.toml import load_toml


def test_version_alignment():
    poetry_version = get_poetry_version()
    assert __version__ == poetry_version


def get_poetry_version() -> Optional[str]:
    path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
    pyproject = load_toml(str(path))
    return pyproject['project']['version']
