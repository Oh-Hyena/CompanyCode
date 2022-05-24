import os
import numpy as np
import time


def top_row():
    for i in range(row_arr):
        arr[0] = "■"

def middle_row():
    for i in range(row_arr):
        arr[int(row_arr/2)] = "■"

def bottom_row():
    for i in range(row_arr):
        arr[-1] = "■"

def left_col():
    for i in range(row_arr):
        arr[i][0] = "■"

def left_top_col():
    for i in range(row_arr):
        if i < int(row_arr/2):
            arr[i][0] = "■"

def left_bottom_col():
    for i in range(row_arr):
        if i >= int(row_arr/2):
            arr[i][0] = "■"

def middle_col():
    for i in range(row_arr):
        arr[i][int(col_arr/2)] = "■"

def right_col():
    for i in range(row_arr):
        arr[i][-1] = "■"

def right_top_col():
    for i in range(row_arr):
        if i < int(row_arr/2):
            arr[i][-1] = "■"

def right_bottom_col():
    for i in range(row_arr):
        if i >= int(row_arr/2):
            arr[i][-1] = "■"

def list_print():
    for i in arr:
        for j in i:
            print(j, end=' ')
        print()

def clear():
    os.system('cls')


if __name__ == "__main__":
    while True:
        row_arr = int(input("행의 길이를 입력해주세요. : "))
        col_arr = int(input("열의 길이를 입력해주세요. : "))

        arr = [["□" for j in range(col_arr)] for i in range(row_arr)]
        arr = np.array(arr)

        input_num = int(input("숫자를 입력해주세요. (0~9) : "))

        if input_num == 0 :
            top_row(), left_col(), right_col(), bottom_row()
            list_print()

        elif input_num == 1 :
            middle_col()
            list_print()

        elif input_num == 2 :
            top_row(), right_top_col(), middle_row(), left_bottom_col(), bottom_row()
            list_print()

        elif input_num == 3:
            top_row(), right_top_col(), middle_row(), right_bottom_col(), bottom_row()
            list_print()

        elif input_num == 4 :
            left_top_col(), middle_row(), middle_col()
            list_print()

        elif input_num == 5:
            top_row(), left_top_col(), middle_row(), right_bottom_col(), bottom_row()
            list_print()

        elif input_num == 6:
            top_row(), left_col(), bottom_row(), right_bottom_col(), middle_row()
            list_print()

        elif input_num == 7:
            left_top_col(), top_row(), right_col()
            list_print()

        elif input_num == 8:
            top_row(), middle_row(), bottom_row(), left_col(), right_col()
            list_print()

        elif input_num == 9:
            middle_row(), left_top_col(), top_row(), right_col(), bottom_row()
            list_print()

        elif input_num > 9:
            print("0~9 외의 숫자를 입력해서 프로그램을 종료합니다.")
            break

        time.sleep(2)
        clear()






