from pathlib import Path
from toml import load, dump


def main():
    files_config = load("web_config.toml")
    include = files_config["files"]["include"]
    exclude = files_config["files"]["exclude"]
    packages = files_config["packages"]
    directories = files_config["directories"]

    files = [
        "/".join(file.parts)
        for directory in directories
        for file in Path(directory).rglob("*.py")
        if file.is_file()
        and not file.name.startswith("__")
        and not file.name.endswith("__")
        and file.name not in exclude
    ]
    files += include

    dct = {"packages": packages, "fetch": [{"files": sorted(files)}]}

    dump(dct, open("pybattle/screen/web/pyscript.toml", "w"))


if "__main__" == __name__:
    main()
