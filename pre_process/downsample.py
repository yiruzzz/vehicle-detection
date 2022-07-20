import cv2
import os


img_dir = r'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/Image'
save_dir = 'D:/dataset/ITCVD/ITC_VD_Training_Testing_set/Training/Image_resize/'
for filename in os.listdir(img_dir):
    imgfile = os.path.join(img_dir, filename)
    im = cv2.imread(imgfile)
    # cv2.imshow('image', im)
    # cv2.waitKey(0)  # 等待任意按键按下
    # h, w = im.shape[0], im.shape[1]
    # print(type(im))
    # img_down = np.zeros((im.shape[0], im.shape[1]))
    # img_down = im[1:h:8, 1:w:8]

   
    # print(im.shape)
    img_down = cv2.resize(im, (im.shape[1]//2, im.shape[0]//2), interpolation=cv2.INTER_AREA)
    # print(img_down.shape)
    img_down = cv2.resize(img_down, (img_down.shape[0]//2, img_down.shape[1]//2), interpolation=cv2.INTER_AREA)
    # print(img_down.shape)
    img_down = cv2.resize(img_down, (img_down.shape[0]*2, img_down.shape[1]*2), interpolation=cv2.INTER_LINEAR)
    # print(img_down.shape)

    # img_down = cv2.pyrDown(im) # 采用该函数得到的结果相比于resize函数更加模糊
    # img_down = cv2.pyrDown(img_down)
    # # img_down = cv2.pyrDown(img_down)
    # img_down = cv2.pyrUp(img_down)
    # img_down = cv2.resize(im, (1333, 800), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(save_dir + filename, img_down)
    # cv2.imshow('01', img_down)
    # cv2.waitKey(0)  # 等待任意按键按下
