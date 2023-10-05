from pybattle.screen.web.create import update, update_player, update_weather
from pybattle.screen.web.input import key_up, key_down, keys_pressing
import asyncio
from pybattle.screen.web.element import Element, document
from pyodide.ffi import create_proxy


async def myLongFunction():
    while True:
        update_weather()
        update_player()
        update()
        await asyncio.sleep(0.07)


document.onkeydown = create_proxy(key_down)
document.onkeyup = create_proxy(key_up)


def get_dir_func(c):
    def y(_):
        async def x():
            keys_pressing.add(c)
            await asyncio.sleep(0.05)
            keys_pressing.remove(c)

        asyncio.ensure_future(x())

    return create_proxy(y)


asyncio.ensure_future(myLongFunction())

Element("up").add_func_callback("click", get_dir_func("w"))

Element("left").add_func_callback("click", get_dir_func("a"))

Element("down").add_func_callback("click", get_dir_func("s"))

Element("right").add_func_callback("click", get_dir_func("d"))
