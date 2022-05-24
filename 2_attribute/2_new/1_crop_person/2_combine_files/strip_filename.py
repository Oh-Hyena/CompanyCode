import os

img_path = r'C:\Users\user\Desktop\unicomnet_code\hyena\attribute\img'

for dir_path, dir_name, file_name in os.walk(img_path):
    for each in file_name:
        file_path = os.path.join(img_path, each)
        new_file_name = each.replace(" ", "")
        new_file_path = os.path.join(img_path,new_file_name)
        os.rename(file_path, new_file_path)

