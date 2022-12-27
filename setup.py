from urllib.parse import parse_qs, urlparse

import requests
from setuptools import find_packages, setup
from shutil import rmtree
from time import sleep


def get_commits_count(owner_name: str, repo_name: str) -> int:
    """Get the number of commits a GitHub repository has."""
    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?per_page=1"
    r = requests.get(url)
    links = r.links
    rel_last_link_url = urlparse(links["last"]["url"])
    rel_last_link_url_args = parse_qs(rel_last_link_url.query)
    rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
    commits_count = int(rel_last_link_url_page_arg)
    return commits_count


name = "PythonDominator"
repo = "Pybattle"
version_ = 1

commits = get_commits_count(name, repo)
while commits > 49:
    version_ += 1
    commits -= 49

version = f'0.{version_}.{commits}'

print(version)


setup(
    name="pybattle",
    version=version,
    url='https://github.com/PythonDominator/Pybattle',
    author='Jacob Ophoven',
    description='A python ascii text art pokemon style game in the terminal using ANSI escape codes.',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
                'colorama',
    ],
)
