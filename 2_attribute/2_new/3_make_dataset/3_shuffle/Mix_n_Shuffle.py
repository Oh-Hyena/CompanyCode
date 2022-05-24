from random import shuffle
import os
import sys


MIX_FIRST_ANNOT_FILE    = r"C:\attribute_3rd_dataset\final_dataset\test_merge_annotation.txt"
MIX_FIRST_IMAGE_FILE    = r"C:\attribute_3rd_dataset\final_dataset\test_common_img_list.txt"
# MIX_LAST_ANNOT_FILE     = r"man_train_merge_annotation.txt"
# MIX_LAST_IMAGE_FILE     = r"man_train_common_img_list.txt"

RESULT_ANNOT_FILE       = r"C:\attribute_3rd_dataset\final_dataset\shuffle\test_merge_annotation.txt"
RESULT_IMAGE_FILE       = r"C:\attribute_3rd_dataset\final_dataset\shuffle\test_common_img_list.txt"

ENCODING_FORMAT         = "utf-8"

class MixAndShuffle:
    def __init__(self):
        self.baseAnnotationList     = []
        self.baseImageList          = []
        self.baseTotalCount         = 0

        self.shuffleAnnotationList  = []
        self.shuffleImageList       = []


    # (1)
    def initialize(self):
        self.load_files()
        self.baseTotalCount = self.get_total_element_count()

        if self.baseTotalCount == 0:
            sys.exit(-1)

    # (2)
    def run(self):
        shuffleIdxList = self.get_shuffle_index_list()

        if shuffleIdxList is None:
            return

        print('\nShuffling.... ', end='\t')
        for eachIdx in range(self.baseTotalCount):
            self.shuffleAnnotationList.append(self.baseAnnotationList[shuffleIdxList[eachIdx]])
            self.shuffleImageList.append(self.baseImageList[shuffleIdxList[eachIdx]])
        print('Done\n')

        self.save_files()

        print("\nProgram DONE")


    def get_shuffle_index_list(self):
        if self.baseTotalCount == 0:
            print(f'is get_total_element_count() Run? - baseTotalCount 0')
            return None

        baseIdxList = [ i for i in range(self.baseTotalCount) ]

        print(f'\nbaseIdxList Len : {self.baseTotalCount}\n\t[ {baseIdxList[:10]} ... ]')

        shuffle(baseIdxList)
        
        print(f'\t\t-> [ {baseIdxList[:10]} ... ]')

        return baseIdxList


    def load_files(self):
        print()
        # Annotation Files
        self.baseAnnotationList += self.open_file_by_list(MIX_FIRST_ANNOT_FILE)
        # self.baseAnnotationList += self.open_file_by_list(MIX_LAST_ANNOT_FILE)

        # Image Files
        self.baseImageList += self.open_file_by_list(MIX_FIRST_IMAGE_FILE)
        # self.baseImageList += self.open_file_by_list(MIX_LAST_IMAGE_FILE)


    def get_total_element_count(self):
        annoCount   = len(self.baseAnnotationList)
        imgCount    = len(self.baseImageList)

        if annoCount == 0 or imgCount == 0:
            print(f'getTotalElementCount FAILED - Count 0')
            return 0
        elif annoCount != imgCount:
            print(f'getTotalElementCount FAILED - Not Matched Count Anno & Image')
            return 0

        return annoCount

    # return FileText List
    def open_file_by_list(self, filePath):
        _resList = []

        if os.path.isfile(filePath) is False:
            print(f'{filePath} is Not Exist - open_text_file FAILED')
            sys.exit(-1)

        with open(filePath, 'r', encoding=ENCODING_FORMAT) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                _resList.append(eachLine)

        print(f'[ {filePath} ] Load Done')
        return _resList


    def save_files(self):
        # Annotation Files
        self.save_files_at_list(RESULT_ANNOT_FILE, self.shuffleAnnotationList)

        # Image Files
        self.save_files_at_list(RESULT_IMAGE_FILE, self.shuffleImageList)


    def save_files_at_list(self, savePath, saveList):
        with open(savePath, 'w', encoding=ENCODING_FORMAT) as f:
            for line in saveList:
                f.write(f"{line}\n")

        print(f'[ {savePath} ] Save Done')


if __name__ == "__main__":
    runProgram = MixAndShuffle()
    runProgram.initialize()
    runProgram.run()