### Vehicle Detection

#### 1. ITCVD Dataset
> Dataset reference: https://aistudio.baidu.com/aistudio/datasetdetail/54674

> Refenrence paper : Vehicle Detection in Aerial Images

> Refenrence link of remote sensing object detection datasets: http://www.javashuo.com/article/p-kkahprhx-sx.html

#### 2. Dataset Pre-processing
Because of the resolution of ITCVD dataset is higher than the test images we bought, the first step should be downsample the dataset according to the following steps:

- Images Downsample: Down sample an image twice and then up sample to get an image with half the original resolution. Code in /pre_process/downsample.py Reference link: https://github.com/caihuaye/Python-OpenCV3/blob/main/HelloOpenCV.ipynb

- Images Clip: Cut the image with the resolution of 1/2 obtained in the previous step into 4 sub images, and the naming example is as follows:

  For example, the original image is named 00000.jpg, and its 4 sub images are 00000_01.jpg, 00000_02.jpg, 00000_03.jpg, 00000_04.jpg. Code in /pre_process/clip.py

- Ground Truth Process: 
  - Description of Ground Truth in ITCVD:
    The size of the matrix for ground truth is Num_vehicle x Num_information.
    
    Num_vehicle describes the number of vehicle in the current picture, and Num_information means the information of each marked vehicle.
    
    In this dataset, the length of Num_information is 6.
    
    The first and second columns denote the coordinate of the upper left corner of the bounding box (x, y).
    
    The third and fourth columns describe the coordinate of the lower right corner of the bounding box (x, y).
    
    The remaining two columns represent orientation information, which is not used for the time being.
    
  - Modify the label.

    As a result of resizing and cliping the original image, the coordinate of every object also need to be changed. Firstly, a label file is divided into four, namely     left-up, right-up, left-bottom, right-bottom, according to the position of objects in the original image. Then all coordinates are divided by 2. Finally the     results are stored in txt format. Code in /pro_process/mat.py.
    
  - Convert txt format to coco format.
  
    There are four terms in coco format, json_dict = {"images": [ ], "type": "instances", "annotations": [ ], "categories": [ ]}. Code in /pro_process/txt2coco.py. Reference link: https://github.com/yiruzzz/NWPU-VHR-10_2_VOC/blob/main/NWPU-VHR-10_2_voc.py and https://github.com/yiruzzz/voc2coco/blob/main/voc2coco.py.
#### 3. Conclusion
At this point, the preparation is completed, then we trained the dataset with mmdetection framework. 
