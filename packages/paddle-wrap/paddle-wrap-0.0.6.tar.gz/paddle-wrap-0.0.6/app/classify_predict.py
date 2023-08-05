# coding:utf-8

import os
from os import path

import numpy as np
import paddlehub as hub
import prettytable as pt

from paddles.wrap import PaddleWrap

test_image_path = "../res/classify/test"

# 直接用PaddleHub提供的数据集
dataset = hub.dataset.Flowers()
label_map = dataset.label_dict()

paddle_wrap = PaddleWrap('resnet_v2_152_imagenet', dataset)

image_array = sorted([path.join(test_image_path, img) for img in os.listdir(test_image_path)])

run_states = paddle_wrap.task.predict(data=image_array)
results = [run_state.run_results for run_state in run_states]

# results = [
#     [1.9348602e-06, 2.4795752e-05, 9.9995911e-01, 7.0063231e-07, 1.3457786e-05],
#     [9.9999833e-01, 4.6691989e-07, 1.1625366e-06, 5.6342643e-08, 1.5247597e-08],
#     [8.7568080e-01, 1.1847176e-01, 5.7732459e-04, 2.5524562e-03, 2.7177909e-03]
# ]

tb = pt.PrettyTable()
tb.field_names = ['NUM', 'FILE', 'PREDICT', 'SCORE']

for batch_result in results:
    # get predict index
    index_array = np.argmax(batch_result, axis=2)[0]
    for i in range(0, len(index_array)):
        index = index_array[i]
        value = batch_result[0][i][index]

        label = label_map[index] if value > 0.95 else ''
        score = ('%.6f' % value)[:6] if value > 0.95 else ''

        tb.add_row([i + 1, image_array[i][image_array[i].rindex('/') + 1:], label, score])

print(tb)

# result = paddle_wrap.task.predict(data=data, return_result=True)
# for i in range(0, len(data)):
#     print('【%s】:\t%s' % (data[i][len('../res/classify/'):], result[i]))
