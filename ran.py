x1 = 5820589730
x2 = 3408759233

seed = 1

for _ in range(100):
    z = x1 * x2 * (seed + 1)
    print(str(z))
    x2 = x2
    x1 = z / 2
