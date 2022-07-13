from copy import copy

helloVal1 = [1, 2, 3]

# helloVal1 의 주소값을 helloVal2 에 그대로 전달함. 
# 그래서 helloVal1 에서 값을 수정하면 helloVal2 은 수정된 값이 출력됨. 
helloVal2 = helloVal1  
helloVal1[1] = 5
print(helloVal2)  # [1, 5, 3]
print(helloVal1)  # [1, 5, 3]

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# helloVal1 의 값을 helloVal2 에 전달함. (주소값이 아닌 값만 전달함)
# 그래서 helloVal1 에서 값을 수정하더라도 각자의 주소값은 다르기 때문에 helloVal2 의 값은 바뀌지 않음.
helloVal3 = helloVal1[:]
helloVal1[1] = 5
print(helloVal3)  # [1, 2, 3]
print(helloVal1)  # [1, 5, 3]

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# copy 모듈을 이용해서 값(주소갑x)만 복사하기
helloVal4 = copy(helloVal1)
helloVal1[1] = 5
print(helloVal4)  # [1, 2, 3]
print(helloVal1)  # [1, 5, 3]

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 두 변수의 값을 서로 바꾸기
helloVal100 = 100
helloVal200 = 200
helloVal100, helloVal200 = helloVal200, helloVal100

print(helloVal100, helloVal200)