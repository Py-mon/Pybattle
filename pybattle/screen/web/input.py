from pybattle.screen.web.element import window


keys_pressing = set()


def key_down(e):
    e = e or window.event
    charCode = e.keyCode or e.which
    charStr = chr(charCode)

    keys_pressing.add(charStr)


def key_up(e):
    e = e or window.event
    charCode = e.keyCode or e.which
    charStr = chr(charCode)

    keys_pressing.remove(charStr)
