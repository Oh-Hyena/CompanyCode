# 예외처리란 오류가 발생했을 때 어떻게 할지 정하는 것이다.

# 기본 형태
"""
try:
    오류가 발생할 수 있는 구문
except Exception as e:
    오류가 발생함
else:
    오류가 발생하지 않음
finally:
    무조건 마지막에 실행
"""

# 현재 시간 출력
import datetime

nowTime = datetime.datetime.now()
strNowTime = nowTime.strftime('%Y/%m/%d')
print(strNowTime)


# 로또 번호 생성기
import random

randomNumber = random.sample(range(1, 46), 6)  # random.sample(리스트, 갯수)
sortedRandomNumber = sorted(randomNumber)
print(sortedRandomNumber)
