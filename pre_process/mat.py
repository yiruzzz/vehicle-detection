import scipy.io as sio
import numpy as np
import os


# data = sio.loadmat("E:\\detection\\GT\\00001.mat")
# print(data.keys())
# # print(data)
#
# data = data["x00000"]
# print(data)
# print(type(data))


# file_list = os.listdir("E:/detection/GT")
# print(file_list)

# root = r'E:/detection/GT'
# save_root = r'E:/detection/TXT'
# for mat_filename in os.listdir(root):
#     if mat_filename.endswith(".mat"):
#         id = mat_filename[:5]
#         # print(mat_filename, id)
#         data = sio.loadmat(os.path.join(root, mat_filename))["x" + id]
#         txt_filename = id + ".txt"
#         save_path = os.path.join(save_root, txt_filename)
#         # print(data, data.shape)
#         for loc in data:
#             l_x, l_y, r_x, r_y = loc[0], loc[1], loc[2], loc[3]
#             # print(l_x, l_y, r_x, r_y)
#             w = r_x - l_x
#             h = r_y - l_y
#             save_data = "(" + str(l_x // 2) + "," + str(l_y//2) + ")" + "," +      "(" + str(r_x//2) + "," + str(r_y//2) + ")" + ",1"
#             print(save_data, save_path)
#             patch_id = cal(loc, w, h)
#             file = open(save_path, mode='a', encoding='utf-8')
#             file.writelines(save_data + "\n")





def cal(loc, w, h):
    l_x, l_y, r_x, r_y = loc[0], loc[1], loc[2], loc[3]
    # l_x, l_y, r_x, r_y = l_x//2, l_y//2, r_x//2, r_y//2
    # print(l_x, l_y, r_x, r_y)
    
    patch_id = "00"

    if l_x <= w//2 and r_y <= h//2: # 左上角区域
        patch_id = "01"

    elif l_x <= w//2 and r_y >= h//2: # 左下角区域
        patch_id = "02"

    elif l_x >= w // 2 and r_y <= h//2: # 右上角区域
        patch_id = "03"

    elif l_x >= w//2 and r_y >= h//2:
        patch_id = "04"

    return patch_id

if __name__ == '__main__':
    root = r'D:\dataset\ITCVD\ITC_VD_Training_Testing_set\Training\GT'
    save_root = r'D:\dataset\ITCVD\ITC_VD_Training_Testing_set\Training\TXT'
    for mat_filename in os.listdir(root):
        if mat_filename.endswith(".mat"):
            id = mat_filename[:5]
            # print(mat_filename, id)
            data = sio.loadmat(os.path.join(root, mat_filename))["x" + id]

            # print(data, data.shape)
            for loc in data:
                l_x, l_y, r_x, r_y = loc[0], loc[1], loc[2], loc[3]
                # print(l_x, l_y, r_x, r_y)
                w = 5616
                h = 3744
                patch_id = cal(loc, w, h)
                if patch_id == "02":
                    l_y -= h//2
                    r_y -= h//2
                elif patch_id == '03':
                    l_x -= w//2
                    r_x -= w//2
                elif patch_id == '04':
                    l_x -= w//2
                    r_x -= w//2
                    l_y -= h//2
                    r_y -= h//2
                save_data = str(l_x // 2) + "," + str(l_y // 2) + "," + str(r_x // 2) + "," + str(r_y // 2) + ",1"
                

                txt_filename = id + "_" + patch_id + ".txt"
                save_path = os.path.join(save_root, txt_filename)
                print(save_data, save_path)
                file = open(save_path, mode='a', encoding='utf-8')
                file.writelines(save_data + "\n")
