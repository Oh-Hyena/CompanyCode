# 오랜만에 구구단
for i in range(2, 10):
    print(f"[ {i}단 ]")
    for j in range(1, 10):
        print(f"{i} * {j} = {i*j}")
    print()


# 간단하게 코드짜기
dataList    = [1, 2, 3, 4, 5] 
resultList1 = [num * 3 for num in dataList]  # resultList.append() 를 할 필요가 없음.
print(resultList1)

resultList2 = [num * 3 for num in dataList if num % 2 == 0]
print(resultList2)

resultList3 = [i*j for i in range(2, 10) for j in range(1, 10)]
print(resultList3)