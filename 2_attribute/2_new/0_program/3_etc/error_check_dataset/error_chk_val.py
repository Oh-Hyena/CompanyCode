import cv2
src = r'/home/keti/attribute_data/1122_attribute_common_PA100K_market1501_39class/img_list/val/val_common_img_list.txt'
dist_file = r'/home/keti/attribute_data/1122_attribute_common_PA100K_market1501_39class/img_list/val/error_list_val.txt'
error_list = []
for list in open(src):
    label = list.strip()
    image = cv2.imread(label)
    if image is None:
        print(label)
        error_list.append(label)

print('end')
i = 0
textfile = open(dist_file,'w')
for list in error_list:
    print(list)
    textfile.write(list+'\n')
    i += 1
print('error_count : ',i)
textfile.close()