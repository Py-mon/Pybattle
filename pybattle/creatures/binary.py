from asyncio import create_task, run, sleep
from os import get_terminal_size, system
from random import choices, randint, random, shuffle
from sys import stdout

# Hide Cursor
stdout.write("\033[?25l")
stdout.flush()

system("cls")


async def update(queue, col):
    for i, num in enumerate(reversed(queue)):
        print(f"\033[{i};{col}H" + num, end="")
    await sleep(random() / 3)


width, height = get_terminal_size()


async def do(col):
    queue = []
    for i in range(100000):
        # if len(queue) + 1 >= height:
        #     del queue[0]
        if i % height == 0:
            queue.clear()

        if randint(1, 12) == 1:
            numbers = choices(["0", "1"], k=randint(3, 7)) 
            for num in numbers:
                color = randint(50, 150)
                queue.append(f"\033[38;2;0;{color};0m" + num)
                await update(queue, col)
        else:
            queue.append(" ")
            await update(queue, col)


async def main():
    every = 3

    lst = list(range(width // every))
    shuffle(lst)
    for col in lst:
        create_task(do(col * every))
    await sleep(500)


run(main())
