

for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)
    
           
    # if i % 3 == 0:
    #     print('Fizz', end='')        
    # if i % 5 == 0:
    #     print('Buzz', end='')
    # elif i % 3 != 0 and i % 5 != 0:
    #     print(i, end='')
    # print()
        