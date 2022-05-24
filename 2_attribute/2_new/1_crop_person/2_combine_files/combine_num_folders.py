import os
import shutil

img_path  = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\test\crop1"
save_path = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\test\500_1"

# 폴더
# (_)언더바 꼭 넣기!
folder_name   = "test1011_"
folder_length = 6

# 파일
file_max = 500
filename_extension = [".jpg", ".jpeg", ".png"]



class divide_files:
    def __init__(self):
        self.folder_num  = 1
        self.file_num    = 1

        self.save_folder_name_list = []


    def make_save_dir(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print("\n저장 경로(new) :", directory)
            else:
                # shutil.rmtree(경로) : 경로 폴더와 파일 모두 지우기
                shutil.rmtree(directory)
                os.makedirs(directory)
                print("\n저장 경로(del->new) :", directory)
        except OSError:
            print("\nError : Creating directory " + directory)


    def make_name(self, length, name):
        name = str(name)
        rotate = int(length) - len(name)

        if rotate > 0:
            for i in range(rotate):
                name = "0" + name
                """
                ohn = 0ohn
                0ohn = 00ohn
                00ohn = 000ohn
                """
        return name


    def make_folder(self):
        if not os.path.isdir(os.path.join(save_path, folder_name + self.make_name(folder_length, self.folder_num))):
            os.mkdir(os.path.join(save_path, folder_name + self.make_name(folder_length, self.folder_num)))


    def make_file(self):
        for (path, dir, files) in os.walk(img_path):
            for filename in files:
                # if filename.endswith(filename_extension):
                _, ext = os.path.splitext(filename)
                if ext in filename_extension:
                    # os.path.join(path, filename)을 os.path.join(save_path, folder_name + make_name(6, folder_num))에 복사하기
                    shutil.copy(os.path.join(path, filename), os.path.join(save_path, folder_name + self.make_name(folder_length, self.folder_num)))
                    self.file_num += 1

                    if self.file_num > file_max:
                        self.folder_num += 1
                        self.file_num = 1
                        os.mkdir(os.path.join(save_path, folder_name + self.make_name(folder_length, self.folder_num) ))

        save_path_list = os.listdir(save_path)

        print("\n저장된 폴더 이름     :", save_path_list)
        print("저장된 폴더 갯수     :", self.folder_num)

        return self.folder_num


    def run(self):
        self.make_save_dir(save_path)
        print("지정한 파일 최대 갯수 :", file_max)
        self.make_folder()
        self.make_file()


if __name__ == "__main__":
    program = divide_files()
    program.run()