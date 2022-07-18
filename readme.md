### Vehicle Detection

#### 1. ITCVD Dataset
> Dataset reference: https://aistudio.baidu.com/aistudio/datasetdetail/54674

> Refenrence paper : Vehicle Detection in Aerial Images

> Refenrence link of remote sensing object detection datasets: http://www.javashuo.com/article/p-kkahprhx-sx.html

#### 2. Dataset Pre-processing
Because of the resolution of ITCVD dataset is higher than the test images we bought, the first step should be downsample the dataset according to the following steps (usually not necessary):

- Images Downsample: Down sample an image twice and then up sample to get an image with half the original resolution. Code in `/pre_process/downsample.py` Reference link: https://github.com/caihuaye/Python-OpenCV3/blob/main/HelloOpenCV.ipynb

- Images Clip: Cut the image with the resolution of 1/2 obtained in the previous step into 4 sub images, and the naming example is as follows:

  For example, the original image is named 00000.jpg, and its 4 sub images are 00000_01.jpg, 00000_02.jpg, 00000_03.jpg, 00000_04.jpg. Code in `/pre_process/clip.py`

- Ground Truth Process: 
  - Description of Ground Truth in ITCVD:
    The size of the matrix for ground truth is Num_vehicle x Num_information.
    
    Num_vehicle describes the number of vehicle in the current picture, and Num_information means the information of each marked vehicle.
    
    In this dataset, the length of Num_information is 6.
    
    The first and second columns denote the coordinate of the upper left corner of the bounding box (x, y).
    
    The third and fourth columns describe the coordinate of the lower right corner of the bounding box (x, y).
    
    The remaining two columns represent orientation information, which is not used for the time being.
    
  - Modify the label.

    As a result of resizing and cliping the original image, the coordinate of every object also need to be changed. Firstly, a label file is divided into four, namely     left-up, right-up, left-bottom, right-bottom, according to the position of objects in the original image. Then all coordinates are divided by 2. Finally the     results are stored in txt format. Code in `/pro_process/mat.py`.
    
  - Convert txt format to coco format.
  
    There are four terms in coco format, `json_dict = {"images": [ ], "type": "instances", "annotations": [ ], "categories": [ ]}`. Code in `/pro_process/txt2coco.py`. Reference link: https://github.com/yiruzzz/NWPU-VHR-10_2_VOC/blob/main/NWPU-VHR-10_2_voc.py and https://github.com/yiruzzz/voc2coco/blob/main/voc2coco.py.
#### 3. Train on YOLOV5
At this point, the preparation is completed to train the dataset with mmdetection framework. But the results are not satisfactory on such small targets like vehicles. So we train the dateset on YOLOV5.

##### 3.1 Dataset Preparation 

Refer to : https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data

- The project should be organized as (Refer to (COCO128)[https://www.kaggle.com/datasets/ultralytics/coco128]):

  ```text
  dataset 
  ├── images
  │   ├── train
  │   │     ├── 00000.jpg
  │   ├──  val
  │   │     ├── 00001.jpg
  │   ├──  test
  │   │     ├── 00002.jpg 
  ├── labels
  │   ├── train
  │   │     ├── 00000.txt
  │   ├──  val
  │   │     ├── 00001.txt
  │   ├──  test
  │   │     ├── 00002.txt 
  │   ├── dataset.yaml
  yolov5
  ```
 
 YOLOv5 assumes `/coco128` is inside a `/datasets` directory next to the `/yolov5` directory. YOLOv5 locates labels automatically for each image by replacing the last instance of `/images/` in each image path with `/labels/`.
 
- Create dataset.yaml

It is the dataset config file that defines 1) the dataset root directory `path` and relative paths to `train` / `val` / `test` image directories (or *.txt files with image paths), 2) the number of classes `nc` and 3) a list of class `names`:
```
# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: /home/yuanlin/CODE/datasets/ITCVD_new  # dataset root dir
train: /home/yuanlin/CODE/datasets/ITCVD_new/images/train  # train images (relative to 'path') 128 images
val: /home/yuanlin/CODE/datasets/ITCVD_new/images/val  # val images (relative to 'path') 128 images
test: /home/yuanlin/CODE/datasets/ITCVD_new/images/test # test images (optional)

# Classes
nc: 1  # number of classes
names: [ 'vehicle' ]  # class names
```
- Create Labels

The YOLO format, with one `*.txt` file per image (if no objects in image, no `*.txt` file is required). The `*.txt` file specifications are:

  - One row per object
  - Each row is `class x_center y_center width height` format.
  - Box coordinates must be in normalized xywh format (from 0 - 1). If your boxes are in pixels, divide `x_center` and `width` by image width, and `y_center` and `height` by image height.
  - Class numbers are zero-indexed (start from 0). 
##### 3.2 Select a Model

We select the (yolov5x)[https://github.com/ultralytics/yolov5/releases] model and download it into `yolov5` directory.

##### 3.3 Train

For example:
```
# Train YOLOv5x on COCO128 for 3 epochs
$ python train.py --img 640 --batch 16 --epochs 3 --data coco128.yaml --weights yolov5x.pt
```
If you want train the model on multiple GPUs, you can modify the parameter `--device` in `/yolov5/train.py`
All training results are saved to `runs/train/` with incrementing run directories, i.e. `/yolov5/runs/train/exp2`, `/yolov5/runs/train/exp3` etc. 

##### 3.4 Inference

Modify the paremeters `source`, `data`, `weights`, and run `/yolov5/detect.py`.
If you want to show more bounding boxes no matter the detection precision, you can modify the parameter `conf-thres` in `/yolov5/detect.py`, which makes it seem that more objects have been detected.
