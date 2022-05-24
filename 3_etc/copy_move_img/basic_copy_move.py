import os
import shutil

path = r'E:\test\image'
new_path = r'E:\test\result4'


# make file list
files = os.listdir(path)

# make result dir
if not os.path.exists(new_path):
    os.mkdir(new_path)


# copy
for file in files:
    if 'pdf' in file:
        shutil.copy(os.path.join(path, file), os.path.join(new_path, file))
        print('{} has been copied in new folder!'.format(file))
        
# # move
# for file in files:
#     if 'jpg' in file:
#         shutil.move(path + file, new_path + file)
#         print('{} has been moved to new folder!'.format(file))

