import inspect
import json
import os
import sys
import traceback
from pathlib import Path


def get_neighbors(directory: Path):
    for file in directory.glob("*"):
        if file.name != "__pycache__":
            yield file


neighs = get_neighbors(
    Path("C:/Users/jacob/Downloads/Programming/Python/Pybattle/Github/pybattle")
)


def get_files(neighs):
    files = []
    for neigh in neighs:
        if neigh.is_dir():
            files += get_files(get_neighbors(neigh))
        files.append(neigh)
    return files


replaces = json.load(open("replaces.json", "r"))  # {'."""': '"""'}

for file in get_files(neighs):
    with open(file, "r") as file_:
        text = file.read()

    for string, replace in replaces.items():
        last_find = 0
        while text.find(string, last_find) != -1:
            index = text.find(string, last_find)
            text = text[:index] + replace + text[index + len(string) :]
            last_find = index

    with open(file, "w") as file_:
        file_.write(text)

# shows you all the functions that dont have docstrings
# for file in get_files(neighs):
#     file: Path
#     with open(file, "r", encoding="utf-8") as file_:
#         text = file_.read()

#         import_name = ".".join(file.parts[8:])[:-3]
#         exec(f"import {import_name}")

#         from_ = ""
#         for value in eval(import_name).__dict__.values():
#             # print(value, type(value))
#             if inspect.isfunction(value):
#                 func = value

#             elif inspect.isclass(value):
#                 for method in value.__dict__.values():
#                     if type(method) in [property, classmethod, staticmethod]:
#                         # func = method
#                         func = eval(f"{value.__name__}.{method.__name__}")
#                 continue
#             else:
#                 continue

#             index = text.find(func.__name__)
#             lineno = text.count("\n", 0, index) + 1

#             # if func.__name__ == "__init__":
#             #     continue

#             print(f"In file: {file} on line {lineno}:\n {func} {from_}")


# for file in get_files(neighs):
#     import_name = ".".join(file.parts[8:])[:-3]
#     exec(f"""import {import_name}""")
#     for key, value in eval(import_name).__dict__.items():
#         if inspect.isclass(value):
#             # print(value.__dict__)
#             for method in value.__dict__.values():
#                 if inspect.ismethod(method) or inspect.isfunction(method):
#                     if method.__doc__ is None:
#                         # method()
#                         pass
#                         # print(
#                         #     f"{method.__name__} in file {file} has no docstring {key}"
#                         # )
