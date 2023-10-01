from create import update, update_player, update_weather
from movement import key_up, key_down
import asyncio
from element import Element, document
from pyodide.ffi import create_proxy


async def myLongFunction():
    while True:
        await update_weather()
        await update_player()
        await update()
        await asyncio.sleep(0.07)


document.onkeydown = create_proxy(key_down)
document.onkeyup = create_proxy(key_up)

asyncio.ensure_future(myLongFunction())
