# -*- coding: utf8 -*-

import os
import re
from os import path

import paddlehub as hub
import prettytable as pt

img_path = "../res/classify"

# set input dict
input_dict = {
    "image": [path.join(img_path, img) for img in os.listdir(img_path)]
}

model_list = [
    'xception71_imagenet',
    'vgg19_imagenet',
    'shufflenet_v2_imagenet',
    'se_resnext101_32x4d_imagenet',
    'resnext50_vd_64x4d_imagenet',
    'resnext50_vd_32x4d_imagenet',
    'resnext50_64x4d_imagenet',
    'resnext50_32x4d_imagenet',
    'resnext152_vd_64x4d_imagenet',
    'resnext152_64x4d_imagenet',
    'resnet_v2_152_imagenet',
    'pnasnet_imagenet',
    'nasnet_imagenet',
    'mobilenet_v2_imagenet',
    'inception_v4_imagenet',
    'googlenet_imagenet',
    'efficientnetb7_imagenet',
    'dpn131_imagenet',
    'densenet264_imagenet',
    'darknet53_imagenet',
    'alexnet_imagenet'
]

field_list = ['MODEL/CLASSIFY']
tb_list = []

max_dict = {}

for model_name in model_list:
    # 创建每行数据格式
    row_array = ['0'] * len(field_list)

    # 首列：模型名称
    row_array[0] = model_name[:model_name.rindex('_')]

    module = hub.Module(name=model_name)
    results = module.classification(data=input_dict)
    # [[{,},],]
    for result in results:
        # [{,},]
        for item in result:
            # {}, 查找最大的匹配率的对象
            k_list = list(item.keys())
            v_list = list(item.values())

            max_value = max(v_list)

            key = k_list[v_list.index(max_value)]
            value = str(max_value)

            if key not in max_dict or max_dict[key] < max_value:
                max_dict[key] = max_value

            # 填充行数据
            index = field_list.index(key) if key in field_list else -1
            if index >= 0:
                row_array[index] = value

            elif max_value >= 0.4:
                # 新添加key，value
                field_list.append(key)
                row_array.append(value)

                # 调整历史数据，从第3行开始填充历史空数据
                if len(tb_list) > 0:
                    for list_raw in tb_list:
                        list_raw.append('0')

    # 添加一行数据
    tb_list.append(row_array)

# pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
pattern = re.compile(r'^[0-9]+\.[0-9]*$')
for column in range(1, len(field_list)):
    max_value = max_dict.get(field_list[column])

    for row in range(0, len(tb_list)):
        value = float(tb_list[row][column])

        # tb_list[row][column] = '%.4f ' % value if value else ' '
        format_value = '*%.6f ' % value if value == max_value else (' %.6f ' % value if value else '')
        tb_list[row][column] = format_value[:7]

# 按行添加数据
tb = pt.PrettyTable()

tb.field_names = field_list
tb._rows = tb_list

tb.align[field_list[0]] = "l"

print(tb)
