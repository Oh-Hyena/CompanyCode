# 여러 개 인자값을 input 하는 경우
def inputManyArgs(*args):
    sum = 0
    for each in args:
        sum += each
    return sum

print(inputManyArgs(1, 2, 3))  # 6


# **kwargs == key word arguments
def printKwargs(**kwargs):
    for k in kwargs.keys():
        if k == "name":
            print(f'당신의 이름은 {kwargs[k]}입니다.')

print(printKwargs(name = '오혜나'))


