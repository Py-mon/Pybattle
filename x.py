x = [8, 10, 11, 11.6, 12, 12.28, 12.5, 12.66, 12.8, 12.91, 13]
y = []


for i in range(len(x)):
    y.append(x[0] - (x[i] - x[0]))

print(x)

print(y)

z = []
for i in range(len(x)):
    z.append(x[i] - y[i])

print(z)

print(sum(z) / len(z))

n = 13
a = 13
print((1 / 11) * n * (1 / 11) * a * 3)

a = 11
print((1 / 11) * a * 3)
