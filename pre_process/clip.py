# !/usr/bin/env python
# coding=utf-8

import numpy as np
import glob, os
import os
# import cv2
from scipy import misc
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

class image_to_patch:
    def __init__(self, x_stride, y_stride, img_path, crop_image_path):
        self.x_stride = x_stride
        self.y_stride = y_stride

        self.img_path = img_path
        self.crop_image_path = crop_image_path

        if not os.path.exists(crop_image_path):   
            os.mkdir(crop_image_path)

    def to_patch(self):
        # read SAR image
        # img_sar = self.imread(sar_path)
        n_sar = 1
        img = Image.open(self.img_path)
        id = os.path.basename(self.img_path)[:5]
        # high, width => equal size
        h, w = img.size

        for x in range(0, h-300, self.x_stride):
            for y in range(0, w-300, self.y_stride):
                box = [x, y, x + self.x_stride, y + self.y_stride]   
                # if x != 0 and y != 0:
                #     box = [x - 200, y - 200, x + self.x_stride, y + self.y_stride]
                sub_img_label = img.crop(box)
                print('====> img save', os.path.join(self.crop_image_path,  str(id) + '_0' + str(n_sar) + '.jpg'))
                sub_img_label.save(os.path.join(self.crop_image_path,  str(id) + '_0' + str(n_sar) + '.jpg'))
                n_sar = n_sar + 1
        img.close()


    def imread(self, path):
        img = Image.open(path)
        return img


if __name__ == '__main__':
    # clip_image_size = (1000, 800)

    img_dir = 'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/Image_resize/'
    crop_image_dir = 'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/Image_clip/'

    for filename in os.listdir(img_dir):
        img_path = os.path.join(img_dir, filename)
        # image to patch
        task = image_to_patch(1404, 936, img_path, crop_image_dir)
        task.to_patch()
