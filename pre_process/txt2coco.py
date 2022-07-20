import os
import glob
import json
import shutil
import numpy as np

# BBox id是从1开始的
START_BOUNDING_BOX_ID = 1

def convert(txt_list, json_file):
    # json文件包含这四类文件信息
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    # 类别是从0开始的
    bnd_id = START_BOUNDING_BOX_ID

    for file_path in txt_list:
        filename = os.path.basename(file_path)[-12:-4] + ".jpg"
        image_id = int(filename[:-4])
        image = {'file_name': filename, 'height': 936, 'width': 1404, 'id': image_id}
        json_dict['images'].append(image)
        # if os.path.basename(file_path)[:-4] == '.txt':
        x_lefts = []
        y_lefts = []
        x_rights = []
        y_rights = []
        names = []

        with open(file_path, 'r') as f:
            contents = f.read()
            objects = contents.split('\n')
            for i in range(objects.count('')):
                objects.remove('')  # 将objects中的空格移除
            for object in objects:
                x_left = int(object.split(',')[0])
                y_left = int(object.split(',')[1])
                x_right = int(object.split(',')[2])
                y_right = int(object.split(',')[3])
                o_width = abs(x_right - x_left) + 1
                o_height = abs(y_right - y_left) + 1
                ann = {'area': o_width*o_height, 'iscrowd': 0, 'image_id':
                image_id, 'bbox':[x_left + 1, y_left + 1, o_width, o_height],
                'category_id': 0, 'id': bnd_id, 'ignore': 0,
                'segmentation': []}
                json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1
            # f.close()        
    cat = {'supercategory': 'none', 'id': 0, 'name': 'vehicle'}
    json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))







txt_dir = r'D:\dataset\ITCVD\ITC_VD_Training_Testing_set\Training\TXT'
txt_list = glob.glob(txt_dir + "\*.txt")
txt_list = np.sort(txt_list)
np.random.seed(100)
np.random.shuffle(txt_list)
train_ratio = 0.5
train_val_ratio = 0.75
test_ratio = 0.25

train_num = int(len(txt_list)*train_ratio)
train_val_num = int(len(txt_list)*train_val_ratio)
test_num = len(txt_list) - train_val_num

txt_list_train = txt_list[:train_num]
txt_list_val = txt_list[train_num:train_val_num]
txt_list_test = txt_list[test_num:]

coco_folder = 'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/'
save_json_train = os.path.join(coco_folder, 'Anns/instances_train.json')
save_json_val = os.path.join(coco_folder, 'Anns/instances_val.json')
save_json_test = os.path.join(coco_folder, 'Anns/instances_test.json')

if os.path.exists(coco_folder + "/train"):
    shutil.rmtree(coco_folder + "/train")
os.makedirs(coco_folder + "/train")  

if os.path.exists(coco_folder + "/val"):
    shutil.rmtree(coco_folder + "/val")
os.makedirs(coco_folder + "/val")

if os.path.exists(coco_folder + "/test"):
    shutil.rmtree(coco_folder + "/test")
os.makedirs(coco_folder + "/test")

convert(txt_list_train, save_json_train)
convert(txt_list_val, save_json_val)
convert(txt_list_test, save_json_test)

img_path = 'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/Image_clip/'

f1 = open("train.txt", "w")
for xml in txt_list_train:
    img = img_path + xml[-12:-4] + ".jpg"
    f1.write(os.path.basename(xml)[:-4] + "\n")
    shutil.copyfile(img, coco_folder + "/train/" + os.path.basename(img))

f2 = open("val.txt", "w")
for xml in txt_list_val:
    img = img_path + xml[-12:-4] + ".jpg"
    f2.write(os.path.basename(xml)[:-4] + "\n") 
    shutil.copyfile(img, coco_folder + "/val/" + os.path.basename(img))

f3 = open("test.txt", "w")
for xml in txt_list_test:
    img = img_path + xml[-12:-4] + ".jpg"
    f3.write(os.path.basename(xml)[:-4] + "\n") 
    shutil.copyfile(img, coco_folder + "/test/" + os.path.basename(img))

f1.close()
f2.close()
f3.close()
