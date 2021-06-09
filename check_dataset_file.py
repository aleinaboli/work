#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import Counter
import xml.etree.ElementTree as et
import shutil

'''
author: BAIY
date: 2021年6月9日

标签只针对txt或xml文件，图片只针对jpg格式。
导出路径中如果有同名文件，此程序会覆盖旧文件，请核实导出路径中旧文件的安全。
所有操作不会改变原始路径下文件内容。
'''

img_path = 'D:\\futi_data_26840'  # 图片路径
ann_path = 'D:\\futi_data_26840'  # 标签路径

ext = '.txt'  # 标签后缀
#ext = '.xml'

output =  True
output_path = 'D:\\1'

fix_filename = True
fix_filename_path = 'D:\\2'


#######


def folder_ext(file_list):
    """
    :param file_list: 图片或者标签路径
    :return: 文件夹中所包含文件类型和个数
    """
    ext_all = []  # 文件后缀列表
    folder = 0  # 文件夹列表

    for file in file_list:
        if '.' in file:  # 如果此项是文件
            f = os.path.splitext(file)
            ext = f[1]
            ext_all.append(ext)
        else:
            folder += 1
    return dict(Counter(ext_all)), folder


i_list = os.listdir(img_path)
a_list = os.listdir(ann_path)

i_ext_dic, i_folder_n = folder_ext(i_list)
a_ext_dic, a_folder_n = folder_ext(a_list)
print(f"图片路径'{img_path}'中文件夹个数：{i_folder_n}")
print(f"文件类型和个数：{i_ext_dic}")
print(f"标签路径'{ann_path}'中文件夹个数：{a_folder_n}")
print(f"文件类型和个数：{a_ext_dic}")
if '.jpg' not in i_ext_dic:
    print(f"'{img_path}'中没有jpg文件")
    exit()
if ('.txt' not in a_ext_dic) and ('.xml' not in a_ext_dic):
    print(f"'{ann_path}'中没有txt或xml文件")
    exit()

label_list = []
match_n = 0
if ext in a_ext_dic:
    for a in a_list:
        if a.endswith(ext):
            name = a.split('.')[0]
            if name + '.jpg' in i_list:
                label_list.append(a)
                match_n += 1
if match_n == 0:
    print(f"'{img_path}'和'{ann_path}没有名称匹配的'.jpg'和'{ext}'文件")
    exit()
else:
    print(f"'.jpg'和'{ext}'文件名匹配有{match_n}个")

if ext == '.txt':
    i = 0
    for txt in label_list:
        size = os.path.getsize(os.path.join(ann_path, txt))
        if size == 0:
            label_list.remove(txt)
            i += 1
    print('空txt文件：', i)
    print('有标签的txt文件个数：', len(label_list))
    if 'classes.txt' in a_list:
        with open(os.path.join(ann_path, 'classes.txt'), "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            print('txt标签类别：')
            print(data)
    else:
        print(f"'{ann_path}'中没有'classes.txt'标签文件")

xml_label = []
fname_ero_list = []

if ext == '.xml':
    i = 0
    for xml in label_list:
        tree = et.parse(os.path.join(ann_path, xml))
        root = tree.getroot()
        if not root.findall('object'):
            label_list.remove(xml)
            i += 1
        else:
            for obj in root.findall('object'):
                rank = obj.find('name').text
                if rank not in xml_label:
                    xml_label.append(rank)

    print('无<object>空xml文件：', i)
    print('有标签的xml文件个数：', len(label_list))
    print('xml标签类别：', xml_label)
    j = 0
    for xml in label_list:
        tree = et.parse(os.path.join(ann_path, xml))
        root = tree.getroot()
        if root.find('filename').text == xml.split('.')[0] + '.jpg':
            continue
        else:
            id = label_list.index(xml)
            fname_ero = label_list.pop(id)
            fname_ero_list.append(fname_ero)
            # label_list.remove(xml)
            print(f"'{xml}'中图片名称和文件名不符")
            j += 1
    print(f'图片名称和文件名不符的xml文件个数：{j}')
    if j != 0:
        print('-----------------------------------------------------------------')
        print(f"检测到有xml中图片名称和文件名不符文件{j}个。")
        print('''如果需要修改xml<filename>并导出，请设置保存路径，修改fix_filename为True。
-----------------------------------------------------------------
        ''')

print(f"*****符合要求的图片和标签数据共有{len(label_list)}对*****")
print('''
-----------------------------------------------------------------
如果要导出匹配的图片和标签，请设置导出保存路径，再修改output为True。
-----------------------------------------------------------------
''')



####数据提取

def output_process():
    print('正在运行匹配项导出程序......')
    if not os.path.exists(output_path):
        print(f"导出路径'{output_path}'不存在。")
        exit()
    if ext == '.txt':
        i = 0
        for txt in label_list:
            shutil.copyfile(os.path.join(ann_path, txt), os.path.join(output_path, txt))
            img = txt[:-3] + 'jpg'
            shutil.copyfile(os.path.join(img_path, img), os.path.join(output_path, img))
            i += 1
        print(f"成功移动图片和标签到'{output_path}'：{i}")
        if 'classes.txt' in a_list:
            shutil.copyfile(os.path.join(ann_path, 'classes.txt'), os.path.join(output_path, 'classes.txt'))
            print(f"成功移动标签类别文件到'{output_path}'")
        else:
            print(f"'{ann_path}'中没有'classes.txt'标签文件")
    if ext == '.xml':
        i = 0
        for xml in label_list:
            shutil.copyfile(os.path.join(ann_path, xml), os.path.join(output_path, xml))
            img = xml[:-3] + 'jpg'
            shutil.copyfile(os.path.join(img_path, img), os.path.join(output_path, img))
            i += 1
        print(f"成功移动图片和标签到'{output_path}'：{i}")
    print()


if output:
    output_process()


def fix_filename_process():
    print('正在运行修正xml文件并导出程序......')
    if ext != '.xml':
        print("所需修正文件不是'.xml'格式。")
        exit()
    if not os.path.exists(fix_filename_path):
        print(f"导出路径'{fix_filename_path}'不存在。")
        exit()
    else:
        for i, ero_xml in enumerate(fname_ero_list):
            xml_path = os.path.join(ann_path, ero_xml)
            tree = et.parse(xml_path)
            root = tree.getroot()
            root.find('filename').text = ero_xml.split('.')[0] + '.jpg'
            new_xml_path = os.path.join(fix_filename_path, ero_xml)
            tree.write(new_xml_path, encoding="utf-8", xml_declaration=True)
            img = ero_xml[:-3] + 'jpg'
            shutil.copyfile(os.path.join(img_path, img), os.path.join(fix_filename_path, img))
        print(f"共修正并导出图片和标签{i+1}对，路径'{fix_filename_path}'")
    print()


if fix_filename:
    fix_filename_process()
