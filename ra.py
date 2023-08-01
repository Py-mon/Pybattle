from random import choices, randint

for col in range(5):
    row = randint(1, 6 )
    is_space = choices([True, False], [1, 5])[0]
    width = choices([1, 2, 3, 4], [10, 20, 2, 3])[0]
    if is_space:
        print(repr(" " * width))
    else:
        print(str(row).rjust(width))
