# -*- coding: utf8 -*-

import paddlehub as hub
import cv2
import os

from os import path

module = hub.Module(name="pyramidbox_lite_mobile_mask")
# module = hub.Module(name="pyramidbox_lite_server_mask")

img_path = '../res/mask'

# set input dict
# input_dict = {
#     "data": [cv2.imread(test_img_path)]
# }
#
# results = module.face_detection(data=input_dict)

# or
input_dict = {
    "image": [path.join(img_path, img) for img in os.listdir(img_path)]
}
"""
data：dict类型，支持data和image两种key，其中：
    key为data，表示value为待检测的图片数据，numpy.array类型，shape为[H, W, C]，BGR格式。
    key为image，表示value为待检测的图片路径。
use_gpu：bool类型，表示是否使用GPU进行预测，需要 配合环境变量 CUDA_VISIBLE_DEVICES使用
batch_size：int类型，表示批量预测时的大小，默认为1，设置越大能够同时处理越多图片，但是会带来更高的显存消耗
shrink：float类型 (0, 1]，用于设置图片的缩放比例，该值越大，则对于输入图片中的小尺寸人脸有更好的检测效果（模型计算成本越高），反之则对于大尺寸人脸有更好的检测效果。
use_multi_scale：bool类型，用于设置是否开启多尺度的人脸检测，开启多尺度人脸检测能够更好的检测到输入图像中不同尺寸的人脸，但是会增加模型计算量，降低预测速度
"""
results = module.face_detection(data=input_dict,
                                use_gpu=False,
                                batch_size=1,
                                shrink=0.5,
                                use_multi_scale=False)
for result in results:
    print(result)
