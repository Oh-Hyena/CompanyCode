def calcSum(scoreList: list) -> int:
    return sum(scoreList)


def calcAvg(scoreList: list) -> float:
    return sum(scoreList) / len(scoreList)


def getEachScoreString(scoreList: list) -> str:
    res = ""
    for each in scoreList:
        res += f"{each} | "
    return res


def printScore(totalDict: dict) -> None:
    for k, v in totalDict.items():
        print(f'{k} | {getEachScoreString(v)}{calcSum(v)} | {calcAvg(v)}')


if __name__ == "__main__":
    # Make Empty Dict
    total_dict = {}

    # Set Score each Person
    total_dict['오혜나'] = [81, 82, 83, 84, 85]
    total_dict['소병준'] = [91, 92, 93, 94, 95]
    total_dict['이세연'] = [71, 72, 73, 74, 75]
    print(total_dict)

    printScore(total_dict)