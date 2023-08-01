from math import factorial

n = 3

lst = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


xs = []
for k in lst:
    x = factorial(n) / (factorial(k) * factorial(k - n))
    print(x)
    xs.append(x)

print(xs, sum(xs) / len(xs))
