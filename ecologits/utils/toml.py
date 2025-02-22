import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def load_toml(file_path):
    with open(file_path, "rb") as f:
        return tomllib.load(f)
