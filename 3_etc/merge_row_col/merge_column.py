import glob
import os
import io

# annotation/img.txt 파일들이 있는 폴더 경로 설정
merge_path = r"C:\Users\user\Desktop\unicomnet_code\test\test1\annotation2"
os.chdir(merge_path)
save_path  = r"C:\Users\user\Desktop\unicomnet_code\test\test1\annotation2\merge_annotation.txt"
encodingFormat = "utf8"


class merge_column:
    def __init__(self):
        # 파일 count 변수, 줄수 count 변수
        self.file_count = 0
        self.line_count = 0


    def confirm_filename(self):
        if os.path.exists("merge_annotation.txt"):
            os.remove("merge_annotation.txt")
            print("merge 저장 파일 이름 : merge_annotation.txt")
        else:
            print("merge 저장 파일 이름 : merge_annotation.txt")


    def merge_txt_file(self):
        self.merge_files = glob.glob("*.txt")
        print("merge 저장 파일 목록 :", self.merge_files)


    def extract_merge_file(self):
        with open(save_path, "wb") as out_file:
            for filename in self.merge_files:
                self.file_count += 1

                with open(filename, "rb") as in_file:
                    out_file.write(in_file.read())

    def merge_count(self):
        print("\n폴더 내 파일 count :", self.file_count)

        self.line_count = open(save_path, "r", encoding=encodingFormat)
        print("파일 내 줄수 count : %d" % (len(list(enumerate(self.line_count)))))


    def run(self):
        print("\n폴더 경로 :", merge_path)

        self.confirm_filename()
        self.merge_txt_file()
        self.extract_merge_file()
        self.merge_count()


if __name__ == "__main__":
    program = merge_column()
    program.run()

