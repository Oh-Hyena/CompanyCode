import sys
import os
import time
import operator


"""
1. 해당 카테고리의 전체 메뉴를 500원 인상시키기

2. 추가 주문받기 (김밥+오뎅+콜라 주문)
   예를 들어 추가주문 하시겠습니까?(y/n) -> 카테고리 선택으로 이동

3. 뒤로가기
   예를 들어 메뉴 선택 -> 카테고리 선택으로
"""

def pick_choice():
    print("[ choice ]")
    print("1. 메뉴 선택하기\n2. 가격 인상하기\n3. 메뉴 추가하기\n4. 메뉴 삭제하기\n0. 프로그램 종료")
    print()
    
    choice_num = int(input("번호를 선택해주세요 : "))
    clear() 

    return choice_num


def pick_category():
    print("[ category ]")
    category_list = []
    for c_index, c_name in enumerate(boki_heaven_dic['category'].keys()):
        print(f"{c_index}. {c_name}", end="  ")
        category_list.append(c_name)
    print()

    print()
    category_num = int(input("category 를 선택해주세요 : "))
    clear()

    return category_list, category_num


def pick_menu(category_list, category_num):
    print(f"[ {category_list[category_num]} ]")
    menu_list = []
    for m_index, m_name in enumerate(boki_heaven_dic['category'][category_list[category_num]].keys()):
        print(f"{m_index}. {m_name}", end="  ")
        menu_list.append(m_name)
    print()

    print()
    menu_num = int(input("menu 를 선택해주세요 : "))
    clear()
    
    return menu_list, menu_num


def your_choice_menu(category_list, category_num, menu_list, menu_num):
    print(f"[ your pick ]")
    final_category = category_list[category_num]
    final_menu = menu_list[menu_num]
    final_price = boki_heaven_dic['category'][category_list[category_num]][menu_list[menu_num]]
    print(f"당신이 선택한 category 는 {final_category} 이고, menu는 {final_menu} 이고, {final_price} 원입니다.")
    print()
    time.sleep(2)

    return final_category, final_menu, final_price


def raise_price(final_category, final_menu):
    change_price = input("가격을 얼마로 인상하실 겁니까? ")
    time.sleep(1)
    print()
    print(f"{final_menu} 는 {change_price} 로 인상되었습니다.")

    boki_heaven_dic['category'][final_category].update({final_menu:change_price})
    time.sleep(2)
    clear()


def add_menu(category_list, category_num):
    add_menu_name = input("추가할 menu 이름을 입력하세요. : ")
    add_menu_price = input("추가할 menu 가격을 입력하세요. : ")
    time.sleep(1)
    print()
    print(f"당신이 추가한 menu 는 {add_menu_name} 이고, 가격은 {add_menu_price} 입니다.")

    boki_heaven_dic['category'][category_list[category_num]].update({add_menu_name:add_menu_price})
    time.sleep(2)
    clear()


def del_menu(final_category, final_menu, final_price):
    print(f"당신이 삭제할 menu는 {final_menu} 이고, 가격은 {final_price} 입니다.")
    print()
    del_answer = input(f"정말로 삭제하시겠습니까?(y/n) : ")
    if del_answer == 'y' or 'Y':
        del boki_heaven_dic['category'][final_category][final_menu]
    print()
    time.sleep(2)
    clear()


def clear():
    os.system('cls')

def program_exit():
    sys.exit()


if __name__ == "__main__":

    boki_heaven_dic = {}

    boki_heaven_dic['category'] = {}
    boki_heaven_dic['category']['김밥'] = {'원조김밥':2500, '치즈김밥':3000, '참치김밥':3500, '땡초김밥':4000}
    boki_heaven_dic['category']['돈까스'] = {'기본돈까스':7000, '더블돈까스':9000, '치킨까스':7500, '생선까스':7500}
    boki_heaven_dic['category']['분식'] = {'우동':5000, '오뎅':4500, '칼국수':6000, '쫄면':7000}
    boki_heaven_dic['category']['식사'] = {'카레덮밥':6000, '참치덮밥':6500, '소불고기덮밥':6500, '제육덮밥':6500}
    boki_heaven_dic['category']['국밥'] = {'콩나물국밥':6000, '육개장':7000, '갈비탕':7000, '설렁탕':7000}
    boki_heaven_dic['category']['사이드'] = {'콜라':1000, '사이다':1000, '공깃밥':1000}

    print(boki_heaven_dic['category'].len("밥"))

    while True:
        # choice 선택
        choice_num = pick_choice()
    
        # choice1 : category와 menu 선택하기
        if choice_num == 1: 
            # category 선택하기
            category_list, category_num = pick_category()

            # menu 선택하기
            menu_list, menu_num = pick_menu(category_list, category_num)
            your_choice_menu(category_list, category_num, menu_list, menu_num)
            clear()

        # choice2 : menu 가격 인상하기
        elif choice_num == 2:
            # category 선택하기
            category_list, category_num = pick_category()

            # menu 선택하기
            menu_list, menu_num = pick_menu(category_list, category_num)
            final_category, final_menu = your_choice_menu(category_list, category_num, menu_list, menu_num)

            # menu 가격 인상하기
            raise_price(final_category, final_menu)

        # choice3 : menu 추가하기
        elif choice_num == 3:
            # category 선택하기
            category_list, category_num = pick_category()

            # menu 추가하기
            add_menu(category_list, category_num)

        # choice4 : menu 삭제하기
        elif choice_num == 4:
            # category 선택하기
            category_list, category_num = pick_category()

            # menu 선택하기
            menu_list, menu_num = pick_menu(category_list, category_num)
            final_category, final_menu, final_price = your_choice_menu(category_list, category_num, menu_list, menu_num)
            clear()

            # menu 삭제하기
            del_menu(final_category, final_menu, final_price)

        elif choice_num == 0: 
            print(f"프로그램을 종료하겠습니다.")
            time.sleep(1)
            print()
            # 프로그램 종료하기
            program_exit()
            




