# 짧은 버전
# import sys
# sys.setrecursionlimit(10000)

def score_sum(score_list):
    total_sum = sum(score_list)
    return total_sum

def score_ave(score_list):
    total_ave = sum(score_list) / len(score_list)
    return total_ave

def extract_name(name_list):
    print(name_list, end=" | ")

def extract_score(score_list):
    for x in range(len(score_list)):
        print(j[x], end=" | ")

def extract_sum_n_ave(total_sum, total_ave):
    print(f"{total_sum} | {total_ave}")



if __name__ == "__main__":

    # main 함수에 한꺼번에 출력!
    print("part1")
    total_dic = {"오혜나": [81, 82, 83, 84, 85], "소병준": [91, 92, 93, 94, 95], "이세연": [71, 72, 73, 74, 75]}

    for i, j in total_dic.items():
        # 이름 출력
        print(i, end=" | ")
        total_sum = sum(j)
        total_ave = total_sum / len(j)

        # 과목별 점수 출력
        for x in range(len(j)):
            print(j[x], end=" | ")

        # 총합과 평균 점수 출력
        print(f"{total_sum} | {total_ave}")
    print()


    # 함수 만들어서 출력!
    # sum, ave, extrack
    print("part2")
    total_dic = {}

    total_dic['오혜나'] = [81, 82, 83, 84, 85]
    total_dic['소병준'] = [91, 92, 93, 94, 95]
    total_dic['이세연'] = [71, 72, 73, 74, 75]

    for i, j in total_dic.items():

        extract_name(i)
        total_sum = score_sum(j)
        total_ave = score_ave(j)
        extract_score(j)
        extract_sum_n_ave(total_sum, total_ave)