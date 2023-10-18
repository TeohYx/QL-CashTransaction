# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:22:46 2023

@author: user
"""
import xml.etree.ElementTree as ET
import os


# 0 -> cashier
# 1 -> customer

def single_xml_to_txt(xml_file, jpg_file, class_names):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    #保存txt文件路径
    txt_file = (os.path.basename(xml_file)[:-4] + '.txt')
    with open(txt_file, 'w') as tf:
        for member in root.findall('object'):
            #从xml获取图像的宽和高
            picture_width = int(root.find('size')[0].text)
            picture_height = int(root.find('size')[1].text)
            class_name = member[0].text
            #类名对应的index
            class_num = class_names.index(class_name)
            box_x_min = int(member[4][0].text)  # 左上角横坐标
            box_y_min = int(member[4][1].text)  # 左上角纵坐标
            box_x_max = int(member[4][2].text)  # 右下角横坐标
            box_y_max = int(member[4][3].text)  # 右下角纵坐标
            
            xy = f"{box_x_min},{box_y_min} {box_x_max},{box_y_max}"
            # 转成相对位置和宽高（所有值处于0~1之间）
#            x_center = (box_x_min + box_x_max) / (2 * picture_width)
#            y_center = (box_y_min + box_y_max) / (2 * picture_height)
#            width = (box_x_max - box_x_min) / picture_width
#            height = (box_y_max - box_y_min) / picture_height
            #print(class_num, x_center, y_center, width, height)
            tf.write(str(class_num) + ' ' + xy + '\n')
            print(str(class_num) + ' ' + xy + '\n')

class_names = ["cashier", "customer"]
single_xml_to_txt("out.xml", "out.jpg", class_names)