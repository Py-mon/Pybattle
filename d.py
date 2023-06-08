import asyncio
from queue import Queue
from time import sleep

# async def print_x_every_5_seconds():
#     while True:
#         print("x")
#         await asyncio.sleep(5)


# async def print_y_every_1_second():
#     while True:
#         pass


# async def main():
#     task1 = asyncio.create_task(print_x_every_5_seconds())
#     task2 = asyncio.create_task(print_y_every_1_second())
#     await task1
#     await task2


# asyncio.run(main())

tasks = Queue()


from threading import Lock


def wait(delay_seconds: float) -> None:
    tasks.get()()
    sleep(delay_seconds)


def x():
    Lock().acquire()
    while True:
        print("x")
        wait(1)


def y():
    while True:
        print("y")
        wait(5)


tasks.put(x)
tasks.put(y)

x()
# y()
