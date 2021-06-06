import os

label_path = 'H:\\data_26840\\labels'
jpg_path = 'H:\\data_26840\\JPEGImages'

label_list = os.listdir(label_path)
jpg_list = os.listdir(jpg_path)

def txt_jpg():
    non = 0
    for i,a  in enumerate(label_list):
        if a.endswith('txt'):
            #list.remove(a)
            img = a[:-3]+'jpg'
            if  img not in jpg_list:
                print('no img:',img)
                non+=1

    print(f'共有{i}个txt文件，缺少对应图片{non}张)')

