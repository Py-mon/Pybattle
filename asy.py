from sys import set_int_max_str_digits

set_int_max_str_digits(9999999)


def reverse(x):
    return int(str(x)[::-1])

def check_pal(number):
    reverse_number = reverse(number)
    return (number == reverse(number), number + reverse_number)

number = 689
total = 0
while True:
    state, new_num = check_pal(number)
    total += 1
    
    if state:
        break
    
    number = new_num

    print(total)

print(number)