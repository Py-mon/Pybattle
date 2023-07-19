from random import choices

n = 10
nums = []
for _ in range(1000000):
    things = choices(range(3, 14), k=n)
    nums.append(max(things))
print(sum(nums) / len(nums))
