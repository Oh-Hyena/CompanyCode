import os

txt_list_path = r'D:\dataset\test_list.txt'
img_list_path = r'D:\0628\dataset\test_list.txt'
saveDir = r'D:\save'


# txt_list 읽어오기
txt_list = []
with open(txt_list_path, 'r', encoding='utf-8') as f:
    for each in f:
        each = each.strip('\n')
        each = each.split('.')[0]
        txt_list.append(each)
        txt_list.sort()
        
        
# img_list 읽어오기
img_list = []
with open(img_list_path, 'r', encoding='utf-8') as f:
    for each in f:
        each = each.strip('\n')
        each = each.split('.')[0]
        img_list.append(each)
        img_list.sort()
        
        
# txt_list 에만 있는 것
# only_txt_list = list(set(txt_list)-set(img_list))
only_txt_list = list(set(txt_list).difference(set(img_list)))


# img_list 에만 있는 것
# only_img_list = list(set(img_list)-set(txt_list))
only_img_list = list(set(img_list).difference(set(txt_list)))


# txt_list 와 img_list 모두에 있는 것
# abb_list = list(set(txt_list) & set(img_list))
abb_list = list(set(txt_list).intersection(set(img_list)))


# only_txt_list 저장하기
onlyTxt_savePath = os.path.join(saveDir, 'only_txt.txt')
with open(onlyTxt_savePath, 'w', encoding='utf-8') as f:
    for each in only_txt_list:
        each = each + '.txt'
        f.write(f"{each}\n")
        

# only_img_list 저장하기
onlyImg_savePath = os.path.join(saveDir, 'only_img.txt')
with open(onlyImg_savePath, 'w', encoding='utf-8') as f:
    for each in only_img_list:
        each = each + '.jpg'
        f.write(f"{each}\n")
        

# txt_list 와 img_list 공통으로 있는 파일 저장하기
TxtImg_savePath = os.path.join(saveDir, 'abb_TxtImg.txt')
with open(TxtImg_savePath, 'w', encoding='utf-8') as f:
    for each in abb_list:
        each_txt = each + '.txt'
        each_img = each + '.jpg'
        f.write(f"{each_txt}\n{each_img}\n")
