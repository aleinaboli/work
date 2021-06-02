# -*- coding:utf-8 -*-
# !/usr/bin/env python
 
import argparse
import json

from labelme import utils
import numpy as np
import glob

'''
***readme***
将此python文件放到与待生成coco_json的文件夹同级，修改dir_name为待生成的文件夹名。

'''

class_name = 'person'
#num_keypoints = 6
dir_name = 'l2c'  #修改为文件夹名称
keypoints_names = ["nose","left_eye","right_eye","left_ear","right_ear",
                    "left_shoulder","right_shoulder","left_elbow","right_elbow","left_wrist",
                    "right_wrist","left_hip","right_hip","left_knee","right_knee",
                    "left_ankle","right_ankle"]
skeleton = [[16,14],[14,12],[17,15],[15,13],[12,13],
                             [6,12],[7,13],[6,7],[6,8],[7,9],
                             [8,10],[9,11],[2,3],[1,2],[1,3],
                             [2,4],[3,5],[4,6],[5,7]]


class MyEncoder(json.JSONEncoder):
 def default(self, obj):
  if isinstance(obj, np.integer):
   return int(obj)
  elif isinstance(obj, np.floating):
   return float(obj)
  elif isinstance(obj, np.ndarray):
   return obj.tolist()
  else:
   return super(MyEncoder, self).default(obj)

class labelme2coco(object):
 def __init__(self, labelme_json=[], save_json_path='./train.json'):
  '''
  :param labelme_json: 所有labelme的json文件路径组成的列表
  :param save_json_path: json保存位置
  '''
  self.labelme_json = labelme_json
  self.save_json_path = save_json_path
  self.images = []
  self.categories = []
  self.annotations = []
  self.label = []
  self.group_id = []
  self.annID = 1
  self.height = 0
  self.width = 0
  self.save_json()

 def data_transfer(self):
    
    for num, json_file in enumerate(self.labelme_json):
        with open(json_file,'r') as fp:
            print(json_file)
            data = json.load(fp)
            print(data)
            self.images.append(self.image(data, num))

            for shape in data['shapes']:
                g_id = shape['group_id']

                id_max = max(g_id, 0)
            for j in range(1,id_max+1):

                #keypoints = [0]*num_keypoints*3
                keypoints = [0]*51
                bbox = []  
                for shape in data['shapes']:
                    g_id = shape['group_id']
                    if g_id == j:

                        label = shape['label']
                        points = shape['points']
                        if label != class_name:
                                i = int(label)-1
                                keypoints[i*3] = int(points[0][0])
                                keypoints[i*3+1] = int(points[0][1])
                                keypoints[i*3+2] = 2
                        elif label == class_name:
                                box = self.label2box(points)

                num_keypoints = int(np.count_nonzero(keypoints,axis=0)/3)

                self.annotations.append(self.annotation(label, num, keypoints, num_keypoints, box))
                print('group:',self.annID)
                self.annID += 1
    self.categories.append(self.categorie(0))


 def image(self, data, num):
     image = {}
     img = utils.img_b64_to_arr(data['imageData'])
     height, width = img.shape[:2]
     img = None
     image['height'] = height
     image['width'] = width
     image['id'] = num + 1
     image['dir_name'] = dir_name
     image['file_name'] = data['imagePath']
     image['license'] = 1
     self.height = height
     self.width = width
     return image
 
 def categorie(self, label):
     categorie = {}
     categorie['supercategory'] = class_name
     #categorie['id'] = len(self.group_id) + 1 # 0 默认为背景
     categorie['id'] =1
     categorie['name'] = class_name
     categorie["keypoints"] = keypoints_names
     categorie["skeleton"] = skeleton
     return categorie


 def annotation(self, label, num, keypoints,num_keypoints, box):
     annotation = {}
     annotation['segmentation'] = [0]
     annotation['num_keypoints'] = num_keypoints
     annotation['area'] = 0
     annotation['iscrowd'] = 0

     annotation['keypoints'] = keypoints
     annotation['image_id'] = num + 1
     annotation['bbox'] = box
     #annotation['area'] = annotation['bbox'][2] * annotation['bbox'][3]
     #annotation['category_id'] = self.getcatid(label)#注意，源代码默认为1
     annotation['category_id'] = 1
     annotation['id'] = self.annID
     return annotation
 
 def getcatid(self, label):
     for categorie in self.categories:
         if label == categorie['name']:
             return categorie['id']
     return 1

 def label2box(self, points):
     left_top_x = round(min(points[0][0],points[1][0]),2)
     left_top_y = round(min(points[0][1],points[1][1]),2)
     right_bottom_x = round(max(points[0][0],points[1][0]),2)
     right_bottom_y = round(max(points[0][1],points[1][1]),2)
     print(left_top_x,left_top_y,right_bottom_x,right_bottom_y)
     coco_box = np.round([left_top_x, left_top_y, right_bottom_x - left_top_x, right_bottom_y- left_top_y],2)
     print(coco_box)
     #return [left_top_x, left_top_y, right_bottom_x - left_top_x, right_bottom_y- left_top_y]
     return coco_box

 def data2coco(self):
     data_coco = {}
     data_coco['images'] = self.images
     data_coco['categories'] = self.categories
     data_coco['annotations'] = self.annotations
     return data_coco


 def save_json(self):
     self.data_transfer()
     self.data_coco = self.data2coco()
     # 保存json文件
     json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4, cls=MyEncoder) # indent=4 更加美观显示
 
#输入 输出
labelme_json = glob.glob('./'+ dir_name +'/*.json')
#labelme_json = glob.glob('./*.json')
#print(labelme_json)
labelme2coco(labelme_json, './'+ dir_name +'.json')
