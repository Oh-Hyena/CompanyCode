def list_print(total):
    # 1차원 리스트 가로 출력
    # for i in range(len(total)):
    #     print(total[i] , end=' ')

    # 2차원 리스트 가로 출력
    # for i in total:
    #     for j in i:
    #         print(j, end=' ')
    #     print()

    # 3차원 리스트 가로 출력
    for i in total:
        for j in i:
            for k in j:
                print(k, end=' |  ')
            print()



if __name__ == "__main__":
    ohn_score = ["오혜나", 81, 82, 83, 84, 85]
    sbj_score = ["소병준", 91, 92, 93, 94, 95]
    lsy_score = ["이세연", 71, 72, 73, 74, 75]

    print(ohn_score)

    total_score = [ohn_score, sbj_score, lsy_score]
    total_dic = {"total": total_score}

    list_print(total_dic.values())