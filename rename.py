# -*- coding:utf-8 -*-
import os

'''

修改xml文件夹路径， 图片文件夹，命名规则，新的xml目录

'''
path = 'H:\\data_26840\\Annotations'     # xml文件夹
img_file_path = 'H:\\data_26840\\JPEGImages'  # 图片文件夹
list = os.listdir(path)

for num, xml in enumerate(list):

    img_name = xml[:-3] + 'jpg'
    img_path = img_file_path + '\\' + img_name
    xml_path = path + '\\' + xml

    print(xml_path)
    new_name = '1' + str(num).zfill(5)     ####新命名规则

    xml_new_name = new_name + '.xml'
    img_new_name = new_name + '.jpg'
    new_xml_path = 'H:\\data_26840\\new_xml\\' + xml_new_name   #新的xml目录，需要新建文件夹写在这个路径下
    new_img_path = img_file_path + '\\' + img_new_name

    #####
    try:
        os.rename(img_path, new_img_path)  # src:原名称  dst新名称d
    except FileNotFoundError:
        print(f'*****not found img:{img_path}')
        continue

    #####
    with open(xml_path, "r") as f1, open(new_xml_path, "w") as f2:
        for line in f1:
            if line[-6:-2] == 'path':
                line = f'    <path>{new_img_path}</path>\n'
            if line[-10:-2] == 'filename':
                line = f'    <filename>{img_new_name}</filename>\n'

            f2.write(line)

print(num)
