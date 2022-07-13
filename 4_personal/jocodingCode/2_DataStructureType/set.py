# 집합(set) 은 출력 순서 자유자재
helloset1 = set([1, 2, 3, 4, 5, 6])
helloset2 = set([4, 5, 6, 7, 8, 9])

# 교집합 (intersection)
helloIntersection1 = helloset1 & helloset2
helloIntersection2 = helloset1.intersection(helloset2)
# print(helloIntersection2)

# 합집합 (union)
helloUnion1 = helloset1 | helloset2
helloUnion2 = helloset1.union(helloset2)
# print(helloUnion2)

# 차집합 (difference)
helloDifference1 = helloset1 - helloset2  # helloset1 에만 있는 것 출력
helloDifference2 = helloset1.difference(helloset2)
helloDifference3 = helloset2 - helloset1  # helloset2 에만 있는 것 출력
helloDifference4 = helloset2.difference(helloset1)
# print(helloDifference4)

# 1개 값만 추가 (add)
helloAdd = helloset1.add(7)  # add 해서 변수에 저장하고 출력하면 None 값 뜸

helloset1.add(7)  # 바로 add해서 add한 set을 출력해야 함
print(helloset1)

# 여러 개 값 추가 (update([]))
helloset1.update([7, 8])  # 리스트 형태로 여러 개 값을 추가해야 함
print(helloset1)

# 1개 값만 삭제 (remove)
helloset2.remove(4)
print(helloset2)