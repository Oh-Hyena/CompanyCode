import os
import sys
from random import shuffle


annotation_file = r""
img_file = r""

shuffle_annotation_file = r""
shuffle_img_file = r""

encoding_format = "utf-8"


class shuffle:
    def __init__(self):
        self.annotation_list = []
        self.img_list = []
        self.total_count = []

        self.shuffle_annotation_list = []
        self.shuffle_img_list = []

    # (1)
    def initialize(self):
        self.load_files()
        self.total_count = self.get_total_count()
        if self.total_count == 0:
            sys.exit(-1)


    def load_files(self):
        print("\n")
        self.annotation_list += self.make_file_list(annotation_file)
        self.img_list += self.make_file_list(img_file)
    

    def make_file_list(self, file_path):
        list = []

        if os.path.isfile(file_path) is False:
            print(f'{file_path} is not exist - open text file failed')
            sys.exit(-1)

        with open(file_path, 'r', encoding=encoding_format) as f:
            for each in f:
                each = each.strip('\n')
                list.append(each)
        
        print(f'[ {file_path} ] load done')

        return list


    def get_total_count(self):
        annotation_count = len(self.annotation_list)
        img_count = len(self.img_list)

        if annotation_count == 0 or img_count == 0:
            print(f'annotation count 0')
            return 0
        elif annotation_count != img_count:
            print(f'not matched annotation count & img count')
            return 0

        return annotation_count


    # (2)
    def run(self):
        shuffle_idx_list = self.get_shuffle_idx_list()
        if shuffle_idx_list is None:
            return
        
        print(f'\nshuffling...', end='\t')
        for each in range(self.total_count):
            self.shuffle_annotation_list.append(self.annotation_list[shuffle_idx_list[each]])
            self.shuffle_img_list.append(self.img_list[shuffle_idx_list[each]])
        print(f'done\n')

        self.save_files()
        print('\nprogram done')

    
    def get_shuffle_idx_list(self):
        if self.total_count == 0:
            print(f'total_count 0')
            return None
        
        idx_list = [i for i in range(self.total_count)]
        print(f'\nidx_list len : {self.total_count}\n\t[ {idx_list[:10]} ... ]')

        shuffle(idx_list)
        print(f'\t\t-> [ {idx_list[:10]} ... ]')

        return idx_list


    def save_files(self):
        self.save_files_list(shuffle_annotation_file, self.shuffle_annotation_list)
        self.save_files_list(shuffle_img_file, self.shuffle_img_list)


    def save_files_list(self, save_path, save_list):
        with open(save_path, 'w', encoding=encoding_format) as f:
            for each in save_list:
                f.write(f'{each}\n')

        print(f'[ {save_path} ] save done')


if __name__ == "__main__":
    run_program = shuffle()
    run_program.initialize()
    run_program.run()

