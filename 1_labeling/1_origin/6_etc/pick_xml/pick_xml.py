import os
import shutil

Rootpath=r"G:\주야간_데이터증강\주야간_class6_data_augmentation\bicycle\unitrain10\data_aug\shearing"
train_dataset_path=os.path.join(Rootpath,"xml")
move_img_path=os.path.join(Rootpath,"copy_xml")
os.mkdir(move_img_path)
file=os.listdir(train_dataset_path)
print(file)
file_list=[]
for i in file:
    #print(i)
    if i.endswith(".xml"):
        print(i)
        path1=os.path.join(train_dataset_path,i)
        shutil.move(path1,move_img_path)