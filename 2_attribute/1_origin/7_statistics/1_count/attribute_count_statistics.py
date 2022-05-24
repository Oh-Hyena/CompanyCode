# TEST = r'E:\nothing\0712\attribute_test\merge_attribute_annotation_66class.txt'
TEST = r'H:\39class_attribute_dataset\3_1st_version\7_val_test_dataset\dataset\PETA\peta_220117_dataset\make_class\Annotation_39_Class.txt'
# TEST_
CLASSNUM = 39
##classnum 83 or 66
index=0

LABEL_NO = [0 for _ in range(CLASSNUM)]
ERROR = []

for line in open(TEST):
    label = line.strip()
    for i in range(CLASSNUM):
        if label[i] == '1':
            LABEL_NO[i] += 1

for i in LABEL_NO:
    # print('index {} : {}'.format(index , i))
    print('{}'.format(i))
    index += 1
