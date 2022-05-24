# 무거운 버전 : 총합과 평균 점수를 다시 기존 딕셔너리에 집어넣어서 출력

def total_list_n_dic():
    total_list = [ohn_dic, sbj_dic, lsy_dic]
    total_dic = {"total": total_list}
    return total_list, total_dic


def name_sore(total_dic):
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
    name_sore(total_dic)
    print()

    # 기존 딕셔너리에 총합과 평균 접수 업데이트하기
    ohn_sum_score, ohn_average_score = sum_n_average_score(ohn_dic)
    sbj_sum_score, sbj_average_score = sum_n_average_score(sbj_dic)
    lsy_sum_score, lsy_average_score = sum_n_average_score(lsy_dic)

    ohn_dic.update(([['sum', [ohn_sum_score]], ["average", [round(ohn_average_score)]]]))
    sbj_dic.update(([['sum', [sbj_sum_score]], ["average", [round(sbj_average_score)]]]))
    lsy_dic.update(([['sum', [lsy_sum_score]], ["average", [round(lsy_average_score)]]]))

    # 두번째 total_list, total_dic 만들기
    second_total_list, second_total_dic = total_list_n_dic()

    # 이름, 과목별 점수, 총합, 형균 점수 출력하기
    print("part2")
    name_score_sum_average(second_total_dic)
    print()