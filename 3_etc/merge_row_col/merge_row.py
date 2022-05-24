import os

# txt 파일이 더 많이 있으면 sub_path3... 만들어줘야 함
sub_path1 = r"C:\Users\user\Desktop\unicomnet_code\test\test3\korean.txt"
sub_path2 = r"C:\Users\user\Desktop\unicomnet_code\test\test3\number.txt"
save_path = r"C:\Users\user\Desktop\unicomnet_code\test\test3\merge_annotation.txt"
encodingFormat = "utf8"


class merge_row:
    def __init__(self):
        self.sub_path1_list = []
        self.sub_path2_list = []

        self.save_list      = []
        self.save_idx_list  = []

    def confirm_filename(self):
        if os.path.exists("merge_annotation.txt"):
            os.remove("merge_annotation.txt")
            print("\nmerge 저장 파일 이름 : merge_annotation.txt")
        else:
            print("\nmerge 저장 파일 이름 : merge_annotation.txt")


    def extract_path1_list(self):
        with open(sub_path1, "r", encoding=encodingFormat) as f1:
            for line1 in f1:
                line1 = line1.strip("\n")
                self.sub_path1_list.append(line1)
        print(f"\nsub1 파일 읽기 : {sub_path1} ", end="\t")
        print("-> done")


    def extract_path2_list(self):
        with open(sub_path2, "r", encoding=encodingFormat) as f2:
            for line2 in f2:
                line2 = line2.strip("\n")
                self.sub_path2_list.append(line2)
        print(f"sub2 파일 읽기 : {sub_path2} ", end="\t")
        print("-> done")


    def run(self):
        print("sub1 폴더 경로1 :", sub_path1)
        print("sub2 폴더 경로2 :", sub_path2)

        self.confirm_filename()

        self.extract_path1_list()
        for idx, each_txt in enumerate(self.sub_path1_list):
            self.save_list.append(each_txt)
            self.save_idx_list.append(idx)
        # print(f"[ save sub1 txt file : {save_path}...]", end="\t")
        # print("done")

        self.extract_path2_list()
        # print(f"[ save sub2 txt file : {save_path}...]", end="\t")

        with open(save_path, "w") as f:
            for each_idx in self.save_idx_list:
                f.write(f"{self.sub_path1_list[each_idx]}, {self.sub_path2_list[each_idx]}\n")
        # print("done")


if __name__ == "__main__":
    program = merge_row()
    program.run()