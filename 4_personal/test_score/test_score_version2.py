# 가벼운 버전 : 총합과 평균 점수를 딕셔너리에 넣지 않고 그냥 바로 출력하기 (해결 못 함)

def total_list_n_dic():
    total_list = [ohn_dic, sbj_dic, lsy_dic]
    total_dic = {"total": total_list}
    return total_list, total_dic


def name_score(total_dic):
    for i, j in total_dic.items():
        for x in j:
            for a, b in x.items():
                print(a, end=" | ")
                for t in range(len(b)):
                    print(b[t], end=' | ')
            print()


def name_score_sum_average(total_dic):
    for i in total_dic.values():
        for j in i:
            print(list(j.keys())[0], end=" | ")
            for x, y in j.items():
                for z in range(len(y)):
                    print(y[z], end=" | ")
            print()

def sum_n_average_score(dic):
    sum_score = 0

    for i in dic.values():
        for j in i:
            sum_score += j
        average_score = sum_score / len(i)

    return sum_score, average_score



if __name__ == "__main__":
    ohn_dic = {"오혜나": [81, 82, 83, 84, 85]}
    sbj_dic = {"소병준": [91, 92, 93, 94, 95]}
    lsy_dic = {"이세연": [71, 72, 73, 74, 75]}

    # 첫번째 total_list, total_dic 만들기
    total_list, total_dic = total_list_n_dic()

    # 이름, 과목별 점수 출력하기
    print("part1")
    name_score(total_dic)
    print()

    # 기존 딕셔너리에 총합과 평균 리턴값
    ohn_sum_score, ohn_average_score = sum_n_average_score(ohn_dic)
    sbj_sum_score, sbj_average_score = sum_n_average_score(sbj_dic)
    lsy_sum_score, lsy_average_score = sum_n_average_score(lsy_dic)

    # 총점, 평균 점수 출력하기
    second_total_list = [[ohn_sum_score, round(ohn_average_score)], [sbj_sum_score, round(sbj_average_score)], [lsy_sum_score, round(lsy_average_score)]]
    for i in second_total_list:
        for sum_n_ave in i:
            print(sum_n_ave, end=' | ')
        print()
    print()

    # 이름, 과목별 점수, 총합, 평균 점수 출력하기
    # print("part2")
    # for i, j in total_dic.items():
    #     for x in j:
    #         for a, b in x.items():
    #             print(a, end=" | ")
    #             for t in range(len(b)):
    #                 print(f"{b[t]}", end=" | ")
    #         for sec in second_total_list:
    #             for sna in range(len(sec)):
    #                 print(f"{sec[sna]}", end=" | ")
    #         print()
    # print()

    print("part2")
    for i, j in total_dic.items():
        for x in j:
            for a, b in x.items():
                # 이름 출력
                print(a, end=" | ")

                for t in range(len(b)):
                    # 과목별 점수 출력
                    print(f"{b[t]}", end=" | ")

            print()
    print()