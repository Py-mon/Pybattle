from js import document, window
from typing import Callable


window = window


class Element:
    def __init__(self, id: str) -> None:
        self._element = document.getElementById(id)

    def edit(self, html: str):
        self._element.innerHTML = html

    def add_func_callback(self, event: str, func: Callable):
        self._element.addEventListener(event, func)
