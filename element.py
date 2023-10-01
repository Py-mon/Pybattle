from js import document, window


class Element:
    def __init__(self, id: str) -> None:
        if id == "body":
            self._element = document.body
        else:
            self._element = document.getElementById(id)

    def edit(self, html: str):
        self._element.innerHTML = html

    def add_event(self, event: str, html):
        self._element.addEventListener(event, html)
