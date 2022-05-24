import os
import cv2 
import numpy as np 
import imgaug as ia
import imgaug.augmenters as iaa
import time


img_path = r'H:\Attribute_dataset관련자료\total_makeAttribute_dataset_290K\original_8K검수전\test\test_img'
img_path2 = r'H:\Attribute_dataset관련자료\total_makeAttribute_dataset_290K\original_8K검수전\test\test_data_aug'
img_list_path = r'H:\Attribute_dataset관련자료\total_makeAttribute_dataset_290K\original_8K검수전\test\img_list.txt'


def strip_file_name(img_path):
    print("\n-> Strip filename")

    for dir_path, dir_name, file_name in os.walk(img_path):
        for each in file_name:
            file_path = os.path.join(img_path, each)
            new_file_name = each.replace(" ", "")
            new_file_path = os.path.join(img_path, new_file_name)
            os.rename(file_path, new_file_path)


def get_img_txt_list(img_list_path):
    img_txt_list = []

    with open(img_list_path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip("\n")
            img_txt_list.append(line)  

    return img_txt_list


def get_img_file_list(img_path, img_txt_list):
    img_path_list = os.listdir(img_path)
    img_file_list = []
    img_name_list = []

    # for each in img_path_list:
    for each in img_txt_list:
        img_file_list.append(os.path.normpath(os.path.join(img_path, each)))
        img_name_list.append(each)
    
    return img_file_list, img_name_list


def get_img_read_list(img_file_list):
    print("\n-> Read img list")

    img_read_list = []
    img_size_list = []

    for each in img_file_list:
        # img = cv2.imread(each)

        # 한글 imdecode하기
        n = np.fromfile(each, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)
        img_read_list.append(img)
    
    return img_read_list


def img_augmentation(img_path2, img_read_list):
    # fliplr 좌우 반전
    # print('\n-> Augment img - fliplr')
    # seq = iaa.Sequential([iaa.Fliplr(1.0)])
    # images_aug = seq.augment_images(img_read_list)
    # save_path = os.path.join(img_path2, 'result_fliplr')

    # flipud 상하 반전
    print('\n-> Augment img - flipud')
    seq = iaa.Sequential([iaa.Flipud(1.0)])
    images_aug = seq.augment_images(img_read_list)
    save_path = os.path.join(img_path2, 'result_flipud')

    # rotate 각도 변경(-15)
    # print('\n-> Augment img - rotate -15')
    # seq = iaa.Sequential([iaa.Affine(rotate=(-15, -15))])
    # images_aug = seq.augment_images(img_read_list)
    # save_path = os.path.join(img_path2, 'result_rotate_-15')

    # rotate 각도 변경(15)
    # print('\n-> Augment img - rotate 15')
    # seq = iaa.Sequential([iaa.Affine(rotate=(15, 15))])
    # images_aug = seq.augment_images(img_read_list)
    # save_path = os.path.join(img_path2, 'result_rotate_15')

    # up 이미지 확대
    # print('\n-> Augment img - img up')

    return images_aug, save_path


def save_img_augmentation(save_path, images_aug, img_name_list):
    print("\n-> Save augmentation img")

    if os.path.isdir(save_path) is False:
        os.makedirs(save_path, exist_ok=True)

    for index, each in enumerate(images_aug):
        # cv2.imwrite(os.path.join(save_path, img_name_list[index]), each)

        # 한글 imencode하기
        ext = os.path.splitext(img_name_list[index])[1]
        result, encode_img = cv2.imencode(ext, each)

        savePath = os.path.join(save_path, img_name_list[index])

        if result:
            with open(savePath, mode='w+b') as f:
                encode_img.tofile(f)


if __name__ == "__main__":
    print('\n-> Start augmenting images')

    start_time = time.time()

    # strip_file_name(img_path)

    img_txt_list = get_img_txt_list(img_list_path)
    img_file_list, img_name_list = get_img_file_list(img_path, img_txt_list)
    img_read_list = get_img_read_list(img_file_list)

    images_aug, save_path = img_augmentation(img_path2, img_read_list)

    save_img_augmentation(save_path, images_aug, img_name_list)

    print('\n-> Complete augmenting images\n')

    end_time = time.time()

    print("working time : " + str(end_time-start_time) + " seconds")