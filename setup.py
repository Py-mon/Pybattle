from math import floor
from os import environ

import toml
from dotenv import find_dotenv, load_dotenv
from github import Github
from setuptools import find_packages, setup

with open("metadata.toml") as f:
    data = toml.load(f)


path = find_dotenv()
load_dotenv(path)


def get_total_changes() -> int:
    g = Github(environ['GITHUB_API_KEY'], environ['PASSWORD'])

    repo = g.get_repo(f"{data['author']['user']['github']}/{data['repo']['name']}")

    total_changes = 0
    for contributor in repo.get_stats_contributors():
        for week in contributor.weeks:
            total_changes += week.a + week.d
    return total_changes


main = 0
if data["version"]["main"]["other"]:
    main = data["version"]["main"]["other"]
elif data["version"]["main"]["alpha"]:
    main = 1
elif data["version"]["main"]["beta"]:
    main = 0


changes = get_total_changes() / 10000
version = floor(changes) // 10 + 1 + data["version"]["update"]["add"]


if data["version"]["update"]["other"]:
    version = data["version"]["update"]["other"]


version = f"0.{version}.{round(changes)}"

print(version)


setup(
    name=data["name"],
    version=version,
    url=data["repo"]["url"],
    author=data["author"]["name"],
    description=data["repo"]["desc"],
    packages=find_packages(),
    python_requires=data["requirements"]["python-version"],
    install_requires=["colorama", "requests"],
    license="GNU",
)
