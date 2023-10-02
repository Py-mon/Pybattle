from web.element import window


# def key_press(e):
#     e = e or window.event
#     charCode = e.keyCode or e.which
#     charStr = chr(charCode)

#     if charStr == "a":
#         m2.left()
#     elif charStr == "d":
#         m2.right()
#     elif charStr == "s":
#         m2.down()
#     elif charStr == "w":
#         m2.up()


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
