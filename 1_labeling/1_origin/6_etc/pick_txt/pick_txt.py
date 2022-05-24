import os
import shutil

Rootpath=r"D:\HN_code\G드라이브_복사본2\7class_밤영상(xml,img)\Unitraindataset\Unitrain\Unitrain10\6class"
train_dataset_path=os.path.join(Rootpath,"valid_dataset")
move_img_path=os.path.join(Rootpath,"txt_move")
os.mkdir(move_img_path)
file=os.listdir(train_dataset_path)
print(file)
file_list=[]
for i in file:
    #print(i)
    if i.endswith(".txt"):
        print(i)
        path1=os.path.join(train_dataset_path,i)
        shutil.move(path1,move_img_path)