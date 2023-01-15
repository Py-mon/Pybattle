import pstats
from os import system


system('python -m cProfile -o binary.txt main.py')


with open('log.log', 'w') as file:
    stats = pstats.Stats('binary.txt', stream=file)
    stats.sort_stats('tottime')
    stats.print_stats()