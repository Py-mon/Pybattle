from setuptools import find_packages, setup
from toml import load
import setuptools


with open("metadata.toml") as f:
    data = load(f)

with open("version.txt") as f:
    version = f.read()

with open("README.md") as readme:
    readme = readme.read()

setup(
    name=data["name"],
    version=version,
    url=data["repo"]["url"],
    author=data["author"]["name"],
    description=data["repo"]["desc"],
    long_description=readme,
    packages=find_packages(),
    python_requires=data["requirements"]["python-version"],
    install_requires=["colorama", "requests", "pygame", "keyboard", "toml"],
    
    # requires: list[str] = ...,
    license="GNU",
    
)
