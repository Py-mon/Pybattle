class Foo:
    def __init__(self, weight):
        self.weight = weight


def total_weight(items):
    return sum(max(item.weight, 0) for item in items)


def percentages(items):
    weight = total_weight(items)
    return [max(item.weight, 0) / weight * 100 for item in items]


x = Foo(50)
y = Foo(30)
z = Foo(20)
x.weight -= 10

all_foos = [x, y, z]
foo_percentages = percentages(all_foos)
print(foo_percentages, sum(foo_percentages))
