import cv2
import os

xml_head = '''<annotation>
    <folder>images</folder>
    <filename>{}</filename>
    <path>{}</path>
    <source>
        <database>Unknown</database>
    </source>  
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    '''
xml_obj = '''
    <object>        
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
    '''
xml_end = '''
</annotation>'''
# LIF
# HUM
# CAR
# BOX
labels = ['LIF', 'HUM', 'CAR', 'BOX']  # 这个是你的标签名字，要修改

path = 'D:\\futi_new'
path_list = os.listdir(path)
path_list.remove('classes.txt')
def two_file():
    cnt = 0
    for a in path_list:
        jpg_name = a.replace('.txt', '.jpg')
        jpg_path = path.replace('labels','images\\') + a.replace('.txt', '.jpg')
        img = cv2.imread(jpg_path)
        img_h, img_w = img.shape[0], img.shape[1]
        head = xml_head.format(str(jpg_name), str(jpg_path), str(img_w), str(img_h))
        #print(head)
        obj = ''
        with open('{}\\{}'.format(path,a), 'r') as f:
            for line in f.readlines():
                yolo_datas = line.strip().split(' ')
                label = int(float(yolo_datas[0].strip()))
                center_x = round(float(str(yolo_datas[1]).strip()) * img_w)
                center_y = round(float(str(yolo_datas[2]).strip()) * img_h)
                bbox_width = round(float(str(yolo_datas[3]).strip()) * img_w)
                bbox_height = round(float(str(yolo_datas[4]).strip()) * img_h)

                xmin = str(int(center_x - bbox_width / 2))
                ymin = str(int(center_y - bbox_height / 2))
                xmax = str(int(center_x + bbox_width / 2))
                ymax = str(int(center_y + bbox_height / 2))

                obj += xml_obj.format(labels[label], xmin, ymin, xmax, ymax)
        with open(jpg_path.replace('.jpg', '.xml'), 'w') as f_xml:
            f_xml.write(head + obj + xml_end)
            cnt += 1
            print(cnt)

def one_file():
    cnt = 0
    for a in path_list:
        if a[-3:] == 'txt':
            jpg_name = a.replace('.txt', '.jpg')
            jpg_path = path +'\\'+ jpg_name
            img = cv2.imread(jpg_path)
            img_h, img_w = img.shape[0], img.shape[1]
            head = xml_head.format(str(jpg_name), str(jpg_path), str(img_w), str(img_h))
            with open('{}\\{}'.format(path, a), 'r') as f:
                obj = ''
                for line in f.readlines():
                    yolo_datas = line.strip().split(' ')
                    label = int(float(yolo_datas[0].strip()))
                    center_x = round(float(str(yolo_datas[1]).strip()) * img_w)
                    center_y = round(float(str(yolo_datas[2]).strip()) * img_h)
                    bbox_width = round(float(str(yolo_datas[3]).strip()) * img_w)
                    bbox_height = round(float(str(yolo_datas[4]).strip()) * img_h)

                    xmin = str(int(center_x - bbox_width / 2))
                    ymin = str(int(center_y - bbox_height / 2))
                    xmax = str(int(center_x + bbox_width / 2))
                    ymax = str(int(center_y + bbox_height / 2))

                    obj += xml_obj.format(labels[label], xmin, ymin, xmax, ymax)
            with open(jpg_path.replace('.jpg', '.xml'), 'w') as f_xml:
                f_xml.write(head + obj + xml_end)
            cnt+=1
    print(cnt)
one_file()
