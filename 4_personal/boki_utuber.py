import os
import sys
import time
import random


def line():
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

def information():
    line()
    print(f"[ 오늘의 컨텐츠 : {contents_name} 송출중 ({round_count+1}회차) ]")
    print(f"♡ 고정 구독자 : {fix_subscriber} 명")
    print(f"♥ 구독자 : {subscriber} 명")
    print(f"♡ 좋아요 : {like_num} 개")
    print(f"♥ 싫어요 : {dislike_num} 개")
    line()

def subscriber_updown(subscriber, round_count):
    if round_count == 1:
        subscriber_updown_num = random.randint(0, 1000)
    else:
        subscriber_updown_num = random.randint(-500, 1000)

    print(f"★ 구독자 : {subscriber_updown_num} 명 추가")
    subscriber += subscriber_updown_num
    return subscriber

def like_updown(like_num):
    like_updown_num = random.randint(0, 100)
    print(f"☆ 좋아요 : {like_updown_num} 개 추가")
    like_num += like_updown_num
    return like_updown_num, like_num

def dislike_updown(dislike_num):
    dislike_updown_num = random.randint(0, 100)
    print(f"★ 싫어요 : {dislike_updown_num} 개 추가")
    dislike_num += dislike_updown_num
    return dislike_updown_num, dislike_num

def subscriber_bonus(subscriber, like_updown_num, dislike_updown_num):
    bonus_updown = like_updown_num - dislike_updown_num
    print(f"☆ 보너스 : {bonus_updown} 개 추가")
    subscriber += bonus_updown
    return subscriber

def subscribe_option(subscriber):
    if subscriber >= 1000000:
        print(f"\n백만 유튜버 복이 성공 : {subscriber} 명")
        sys.exit()
    elif subscriber <= 0:
        print(f"\n백만 유튜버 복이 실패")
        sys.exit()

def fix_subscribe(subscriber, paid_item):
    if round_count in round_count_list:
        # if subscriber in subscriber_count_list:
        paid_item += 1

        line()
        print(f"구독자 {subscriber} 명 달성!")
        print(f"당신은 프리미엄 컨텐츠 유료템 구매 가능하십니다.")
        print(f"현재 유료템 수량 : {paid_item} 개")
        buy_paid_item = input("구매하시겠습니까?(y/n) : ")

        if buy_paid_item == "y":
            paid_item -= 1
            fix_subscriber = subscriber * 0.1

            subscriber += round(fix_subscriber)
            print(f"당신은 프리미엄 컨텐츠 유료템을 구매하셨습니다.")
            print(f"◑ 현재 유료템 수량 : {paid_item} 개")
            print(f"◐ 고정 구독자 수   : {fix_subscriber} 명")


if __name__ == "__main__":
    subscriber     = 0
    fix_subscriber = 0

    like_num       = 0
    dislike_num    = 0
    bonus_num      = 0

    round_count    = 0
    paid_item      = 0

    round_count_list      = [x*10 for x in range(1,1000)]
    subscriber_count_list = [x*5000 for x in range(1, 200)]

    channel_name = input("유튜버 채널 이름을 입력해주세요 : ")
    contents_name = input("오늘의 컨텐츠 이름을 입력해주세요 : ")

    while True:
    # for i in range(20):
        information()
        round_count += 1
        time.sleep(2)

        subscriber                      = subscriber_updown(subscriber, round_count)
        like_updown_num, like_num       = like_updown(like_num)
        dislike_updown_num, dislike_num = dislike_updown(dislike_num)
        subscriber                      = subscriber_bonus(subscriber, like_updown_num, dislike_updown_num)

        # subscriber 조건
        subscribe_option(subscriber)

        if round_count in round_count_list:
        # if subscriber in subscriber_count_list:
            paid_item += 1

            line()
            print(f"구독자 {subscriber} 명 달성!")
            print(f"당신은 프리미엄 컨텐츠 유료템 구매 가능하십니다.")
            print(f"현재 유료템 수량 : {paid_item} 개")
            buy_paid_item = input("구매하시겠습니까?(y/n) : ")

            if buy_paid_item == "y":
                paid_item -= 1
                fix_subscriber = subscriber*0.1

                subscriber += round(fix_subscriber)


