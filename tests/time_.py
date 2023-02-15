import pstats
from os import system, remove

# The file that it will test the speeds on
run_file = 'main.py'

# The file it will make temporarily to store binary data.
binary_data_file = 'binary.txt'

system(f'python -m cProfile -o {binary_data_file} {run_file}')

# Takes binary_data_file and translates it into text in time.log
with open('time.log', 'w') as file:
    stats = pstats.Stats('binary.txt', stream=file)
    stats.sort_stats('tottime')
    stats.print_stats()

# Removes the now useless binary file
remove('binary.txt')
