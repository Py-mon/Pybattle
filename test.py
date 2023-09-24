print("_◌̲* ")
#'_"̲*'◌


# H *̲*

# _̲*
# x = 50

# # 1/4, 1/3, 1/2, 1, 2/1
# print(x)
# x1 = round(x * 2 - (x * (1 / 4)))
# print(x1, x * 2, x * 2 - x1)

# x2 = round(x * 3 - (x1 * (1 / 3)))
# print(x2, x * 3, x * 3 - x2)

# x3 = round(x * 4 - (x2 * (1 / 2)))
# print(x3, x * 4, x * 4 - x3)

# x4 = round(x * 5 - (x3 * (2 / 3)))
# print(x4, x * 5, x * 5 - x4)

# x5 = round(x * 6 - (x4 * (3 / 5)))
# print(x5, x * 6, x * 6 - x5)

# x6 = round(x * 7 - (x5 * (4 / 7)))
# print(x6, x * 7, x * 7 - x6)

# x5 = round(x * 6 - (x4 * (1 / 1)))
# print(x5, x * 6, x * 6 - x5)

# x6 = round(x * 7 - (x5 * (1 / -1)))
# print(x6, x * 7, x * 7 - x6)


# bad 33%,  1/3, +2/3, +2/4, +2/5
# good 50%  1/3


# x = 1 / 3
# print(x)

# x1 = x + (2 / 3) * x
# print(x1, x * 2 - x1)

# x2 = x1 + (2 / 4) * x1
# print(x2, x * 3 - x2)

# x3 = x2 + (2 / 5) * x2
# print(x3, x * 4 - x3)
# print()

# x = 1 / 3
# print(x)

# x1 = x + (2 / 3) * x
# print(x1, x * 2 - x1)

# x2 = x * 2 + (2 / 4) * (x * 2)
# print(x2, x * 3 - x2)

# x3 = x * 3 + (2 / 5) * (x * 3)
# print(x3, x * 4 - x3)
# print()


# start = 1 / 2
# y = 8  # the nth that is behind by 1/3

# y = (y - 1) ** 2


# def x(n):
#     return start * n * (y / (y + n - 1))  # ?


# for i in range(1, 12):
#     print(i, round(x(i), 3), start * i - x(i))


#       -0,   -10
# 33%, 66%,  100%
# 50%, 100%, 150%

#       -5,   -15
# 33%, 61%,  85%
# 50%, 95%, 135%

# x = 1 / 3
# print(x)

# x1 = x + (2 / 3) * x
# print(x1, x * 2 - x1)

# x2 = x * 2 - (2 / 4) * x
# print(x2, x * 3 - x2)

# x3 = x * 3 - (2 / 5) * x
# print(x3, x * 4 - x3)


# x3 = x2 + (2 / 5) * x2
# print(x3, x * 4 - x3)

from math import log

level = 1

level_points = {"attack": 1}
bases = {"attack": 100}


levels_bonus = level_points


level = 2
level_points = {"attack": 1}
for stat, mult in levels_bonus.items():
    levels_bonus[stat] *= level_points[stat]

level = 3
level_points = {"attack": 1}
for stat, mult in levels_bonus.items():
    levels_bonus[stat] *= level_points[stat]

level = 4
level_points = {"attack": 1}
for stat, mult in levels_bonus.items():
    levels_bonus[stat] *= level_points[stat]

level = 6
level_points = {"attack": 1}
for stat, _ in levels_bonus.items():
    levels_bonus[stat] *= level_points[stat]

# level = 3
# level_points = {"attack": 1.2}
# for stat, mult in levels_bonus.items():
#     levels_bonus[stat] *= level_points[stat]

# 1.1 -> 7
# 1.2 -> 3.5


# 2 -> 1
# 4 -> 0.5 -> 58%, 100%, 132%
# 6 -> 0.386852807234542
# 8 -> 1/3


# log(2, b)/y=100


def get_stat(stat: str):
    return bases[stat] * (level_points[stat] * (log(level + 1, 4)) / 0.5)


def get_stat(stat: str):
    return bases[stat] * (level_points[stat] * (level**2 / 25)) + 99


def get_stat(stat: str):
    return bases[stat] * (level_points[stat] * 1.1 ** (level - 1))


# print(1.1**(1-1))
# print(1.1**(2-1))
# print(1.1**(3-1))
# print(1.1**(4-1))
# print(1.1**(5-1))
print(get_stat("attack"))

# for n in range(-2, 3):
#     numerator, denominator = 2, 2
#     if n < 0:
#         numerator, denominator = denominator, numerator
#         denominator -= n / 1.5
#     else:
#         numerator += n
#         # 3x = 5.5
#     # 2/3 4/6, 3/4.5
#     print(n, numerator, "/", denominator, "=", numerator / denominator)


for n in range(-4, 4):
    numerator, denominator = 2, 2
    if n < 0:
        x = 1 / ((numerator - n) / denominator)

    else:
        x = (numerator + n) / denominator
        # 3x = 5.5
    # 2/3 4/6, 3/4.5
    print(n, numerator, "/", denominator, "=", x)


# -2 = 0.50
# -1 = 0.75
# 0  = 1.00
# 1  = 1.50
# 2  = 2.00

# -2 = ????
# -1 = ????
# 0  = 1.00
# 1  = 1.33
# 2  = 1.66


# -2 -> 1/(2/3)
# -1 -> 1/(1/3)
#  0 -> 1
#  1 -> 1 + 1/3
#  2 -> 1 + 2/3


# -2 -> 1/(2/3)
# -1 -> 1/(1/3)
#  0 -> 1
#  1 -> 1 + 1/3
#  2 -> 1 + 2/3


# 33%
# 66%
# 100% ->

# -1
# 1
# 0.5 -> 2x less
# 2 -> 2x more
# 0.75 -> 1.5x less
# 1 -> 1

# 0.5 -> 50%
# 2 -> 200%


# 0.75 -> 75%
# 1.5 -> 150%

# 1 -> 1

# print(1 - 1 / 3 ** (1 / -2))


# -1 -> 0.6666
# -1 -> 0.6666
#

# print((4 / 3) ** (-2))


```
   __╱╲       _⎽⎼⎼⎼⎼⎽_  
  ╱ ,  \____ ╱       ╲ 
  \_____    ╲│    ╷  │ 
 _╷____/ ____ ╲   │  ╱ 
│   │___╱    ╲ ╲  │_╱  
 ╲_╱ ___|      │ ╱     
    ╱____╲_____╱╱   
    __/\      _─────_  
   / ,  \___ /       \ 
   \____    \|    /  | 
 _|____/ ____ \   |  / 
|   |___/    \ \  |_/  
 \_/ ___|      | /      
    /____\_____//    
```
  _    _        
 ( \  / )       
  \ \/ /        
  |, , \        
  |     \       
  /     \       
 |  \ /  \ _\/_ 
 \     /    /   
__\_ __\___/    
```
```
  _---_               
<< ,   \_____         
  \   /      \__       
   |  \________/=====- 
    \________/         
        __|_     
```