import os

#0329 Data정제 98000장 test
MAIN_DIR = r'D:\HN_code\인수인계서\20210810_박주희인수인계서_검색\3. 어트리뷰트 데이터셋 제작(83class,66class)\예시\dataset\66annotation'
SRC_DIR =  MAIN_DIR + r'\merge_attribute_annotation_66class.txt'
COMMON_DIR = MAIN_DIR + r'\66_common_attribute_annotation.txt'
HEAD_DIR = MAIN_DIR + r'\66_head_attribute_annotation.txt'
UPPER_DIR = MAIN_DIR + r'\66_upper_attribute_annotation.txt'
LOWER_DIR =MAIN_DIR + r'\66_lower_attribute_annotation.txt'

common_labels = []
head_labels = []
upper_labels = []
lower_labels = []
index = 0
for line in open(COMMON_DIR):
    label = line.strip()
    common_labels.append(label)
    if line == None :
        break
for line in open(HEAD_DIR):
    label = line.strip()
    head_labels.append(label)
    if line == None :
        break
for line in open(UPPER_DIR):
    label = line.strip()
    upper_labels.append(label)
    if line == None :
        break
for line in open(LOWER_DIR):
    label = line.strip()
    lower_labels.append(label)
    if line == None :
        break
print(common_labels[0],head_labels[0], upper_labels[0],lower_labels[0])
merge_labels = []
print(common_labels[0],head_labels[0], upper_labels[0],lower_labels[0])
for i in range(len(common_labels)) :
    merge_labels.append(common_labels[i] + head_labels[i] + upper_labels[i] + lower_labels[i])
print (merge_labels[0])

f = open(SRC_DIR, "w")
f.write('\n'.join(merge_labels))
f.close()
