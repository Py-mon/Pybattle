from math import floor

import requests_cache
import toml
from github import Github
from setuptools import find_packages, setup

with open("metadata.toml") as f:
    data = toml.load(f)


def get_total_changes():
    requests_cache.install_cache("github_cache", expire_after=100000)

    g = Github(data["api-key"])

    repo = g.get_repo(f"{data['author']['user']['github']}/{data['repo']['name']}")

    try:
        commits = repo.get_commits()
    except requests_cache.NotFoundError:
        # If the cache doesn't have the commits, retrieve them from the API and store them in the cache
        commits = repo.get_commits()
        requests_cache.cache_response(commits)

    total = 0

    for commit in commits:
        print(total)
        total += commit.stats.total

    return total


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
