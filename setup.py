from setuptools import setup, find_packages

setup(
    name="ecologits",
    version="0.1.0",
    packages=find_packages(include=["ecologits", "ecologits.*"]),
    include_package_data=True,
    install_requires=[],
)
