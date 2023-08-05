# coding:utf-8

import os

import paddlehub as hub

from paddles.wrap import PaddleWrap

# 直接用PaddleHub提供的数据集
dataset = hub.dataset.Flowers()
paddle_wrap = PaddleWrap('resnet_v2_152_imagenet', dataset)

data = ['../res/classify/daisy/0002.jpg',
        '../res/classify/rose/0001.jpg',
        '../res/classify/test/0002.jpg']

result = paddle_wrap.task.predict(data=data, return_result=True)

for i in range(0, len(data)):
    print('【%s】:\t%s' % (data[i][len('../res/classify/'):], result[i]))
