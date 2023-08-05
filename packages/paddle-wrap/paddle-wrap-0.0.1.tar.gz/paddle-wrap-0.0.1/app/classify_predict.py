# coding:utf-8

import os
from os import path

import paddlehub as hub

from paddles.wrap import PaddleWrap

print(":: PWD: %s" % os.getcwd())

# 直接用PaddleHub提供的数据集
dataset = hub.dataset.Flowers()
paddle_wrap = PaddleWrap('resnet_v2_152_imagenet', dataset)

if paddle_wrap.in_aistudio:
    home_abspath = os.environ['HOME']

    data = [path.join(home_abspath, 'res/classify/daisy/0002.jpg'),
            path.join(home_abspath, 'res/classify/rose/0001.jpg')]
else:
    data = ["../res/classify/daisy/0002.jpg",
            "../res/classify/rose/0001.jpg"]
result = paddle_wrap.task.predict(data=data, return_result=True)
print(result)
