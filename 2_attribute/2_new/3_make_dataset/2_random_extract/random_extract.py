from random import randint

annotation_path = r"C:\Users\user\Desktop\unicomnet_code\test\test1\condition_merge_annotation.txt"
img_path = r"C:\Users\user\Desktop\unicomnet_code\test\test1\condition_common_img_list.txt"

save_annotation_path = r"C:\Users\user\Desktop\unicomnet_code\test\test1\merge_annotation2.txt"
save_img_path = r"C:\Users\user\Desktop\unicomnet_code\test\test1\img_list2.txt"

# utf8 / euckr
encoding_format = "euckr"

# 랜덤으로 뽑고 싶은 갯수 / 원본 txt 파일에서 몇 %를 추출할 건지
over_count      = 50
extract_percent = 5


class random_extract:
    def __init__(self):
        self.annotation_txt_list                = []
        self.img_txt_list                       = []

        self.extract_random_annotation_txt_list = []
        self.extract_random_idx_list            = []

        self.total_object_sum_list              = []
        self.extract_object_sum_list            = []
        
        self.class_num = 0  # 클래스 갯수
        self.try_count = 1  # 재시도 횟수


    # 클래스 갯수 세는 함수
    def count_class_num(self):
        if not self.annotation_txt_list:
            print("Error : not annotation.txt")
            return False

        if self.class_num != 0:
            return True

        # class 갯수 = 어노테이션 텍스트 1번째 리스트 길이(갯수)
        self.class_num = len(self.annotation_txt_list[0])
        print("class 갯수 :", self.class_num)

        return True


    def check_over_count(self, check_object_sum):
        # over_count 넘으면 True, over_count 미달이면 False
        if check_object_sum >= over_count:
            return True
        else:
            return False


    # 클래스별 전체 합계 구하는 함수
    def count_total_object_sum(self):
        if not self.annotation_txt_list:
            print("Error : not annotation.txt")
            return False
        
        # 클래스 갯수를 먼저 구해야 함
        if self.count_class_num() is False:
            return False

        # 전역 변수 선언과 초기화
        for i in range(0, self.class_num):
            globals()[f"{i}번째 class 총 합"] = 0

        print("annotation.txt 전체 갯수 :", len(self.annotation_txt_list))

        # class별 총 합 계산
        for each in self.annotation_txt_list:
            for i in range(0, self.class_num):
                globals()[f"{i}번째 class 총 합"] += int(each[i])

        # class별 총 합 계산 후 저장
        for i in range(0, self.class_num):
            self.total_object_sum_list.append(globals()[f"{i}번째 class 총 합"])

        return True

    # 클래스별 추출한 합계 구하는 함수
    def count_extract_object_sum(self):
        if not self.extract_random_annotation_txt_list:
            print("Error : not extract_annotation.txt")
            return False

        # 클래스 갯수를 먼저 구해야 함
        if self.count_class_num() is False:
            return False

        # 전역 변수 선언과 초기화
        for i in range(0, self.class_num):
            globals()[f"추출한 {i}번째 class 총 합"] = 0

        print("extract_annotation.txt 전체 갯수 :", len(self.extract_random_annotation_txt_list))

        # 추출한 class별 총 합 계산
        for each in self.extract_random_annotation_txt_list:
            for i in range(0, self.class_num):
                globals()[f"추출한 {i}번째 class 총 합"] += int(each[i])

        # over_count 미달인지 체크
        for i in range(0, self.class_num):
            result = globals()[f"추출한 {i}번째 class 총 합"]
            # result가 over_count 미달이면
            if self.check_over_count(result) is False:
                print(f" -> 실패! 추출한 {i}번째 class 갯수 미달 : {result} / {over_count}")
                return False

        # 추출한 class별 총 합 계산 후 저장
        for i in range(0, self.class_num):
            self.extract_object_sum_list.append(globals()[f"추출한 {i}번째 class 총 합"])

        return True


    def make_annotation_txt_list(self):
        with open(annotation_path, "r", encoding=encoding_format) as f1:
            for line1 in f1:
                line1 = line1.strip("\n")
                self.annotation_txt_list.append(line1)


    def make_img_txt_list(self):
        with open(img_path, "r", encoding=encoding_format) as f2:
            for line2 in f2:
                line2 = line2.strip("\n")
                self.img_txt_list.append(line2)


    def show_result(self):
        print("\nClassIdx        |  TotalSum        |  ExtractSum      |  %")
        print("------------------------------------------------------------------------")
        for i in range(0, self.class_num):
            class_idx = i+1
            each_percent = (self.extract_object_sum_list[i] / self.total_object_sum_list[i]) * 100
            print(f"{class_idx:<16}|  {self.total_object_sum_list[i]:<16}|  {self.extract_object_sum_list[i]:<16}|  {round(each_percent, 2)}%")
        print("------------------------------------------------------------------------\n")

        extract_real_percent = (len(self.extract_random_annotation_txt_list) / len(self.annotation_txt_list)) * 100
        print(f"조건              : {over_count}개, {extract_percent}%")
        print(f"총 시도           : {self.try_count}번")
        print(f"원본 txt 파일 줄수 : {len(self.annotation_txt_list)}개")
        print(f"추출 txt 파일 줄수 : {len(self.extract_random_annotation_txt_list)}개 ({round(extract_real_percent, 2)}%)")


    def run(self):
        self.make_annotation_txt_list()
        self.count_total_object_sum()

        while True:
            print(f"\n[ {self.try_count} 번째 시도 ]")

            # try 할 때마다 초기화
            self.extract_random_annotation_txt_list.clear()
            self.extract_random_idx_list.clear()

            random_num = 0

            for idx, annotation in enumerate(self.annotation_txt_list):
                random_num = randint(1, 100)

                # random_num = 50 / extract_percent = 10 이라면
                # 여기서 정한 extract_percent 만큼 추출
                if random_num <= extract_percent:
                    self.extract_random_annotation_txt_list.append(annotation)
                    self.extract_random_idx_list.append(idx)

            # print(" -> extract 끝")

            if self.count_extract_object_sum() is True:
                print(" -> extract 성공!")
                break

            self.try_count += 1

        print(f"\nannotation.txt 파일 저장 경로 : {save_annotation_path}")

        with open(save_annotation_path, "w") as f1:
            for line1 in self.extract_random_annotation_txt_list:
                f1.write(f"{line1}\n")

        self.make_img_txt_list()
        print(f"img_list.txt   파일 저장 경로 : {save_img_path}")

        with open(save_img_path, "w") as f2:
            for idx in self.extract_random_idx_list:
                f2.write(f"{self.img_txt_list[idx]}")

        self.show_result()


if __name__ == "__main__":
    program = random_extract()
    program.run()



