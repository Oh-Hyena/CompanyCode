
# lambda 함수(1)
def add1(a, b):
    return a+b

add1 = lambda a, b: a+b
print(add1(1, 2))


# lambda 함수(2)
myList = [lambda a, b: a+b, lambda a, b: a*b]
add2 = myList[0](1, 2)
print(add2)




