import cv2 
import os
import numpy as np


img_dir = 'D:/MapTileDownload/OutPut/biying_220711152413_L19/results/'
output_file = 'D:/MapTileDownload/OutPut/biying_220711152413_L19/results/m9.tif'

# 先竖着拼接
imgs = sorted(os.listdir(img_dir), key = lambda x : int(x.split('.')[0]))
# print(imgs)
pic = []
for i in range(216, 243): # 修改要拼接的图片序号范围
    image_dir = os.path.join(img_dir, imgs[i])
    print(image_dir)
    image = cv2.imread(image_dir)
    print(image.shape)
    pic.append(image)

merge_pic = np.vstack(pic)
print(merge_pic.shape)
cv2.imwrite(output_file, merge_pic)

# 最终横着拼接成大图
# imgs = sorted(os.listdir(img_dir))
# # print(imgs)
# pic = []
# for i in range(len(imgs)):
#     image_dir = os.path.join(img_dir, imgs[i])
#     print(image_dir)
#     image = cv2.imread(image_dir)
#     print(image.shape)
#     pic.append(image)