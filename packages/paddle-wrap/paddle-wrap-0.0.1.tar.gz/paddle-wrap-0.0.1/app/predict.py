# -*- coding: utf8 -*-

import os
from os import path

import paddlehub as hub

module = hub.Module(name="xception71_imagenet")

img_path = "../res/classify"

# set input dict
input_dict = {
    "image": [path.join(img_path, img) for img in os.listdir(img_path)]
}

# execute predict and print the result
results = module.classification(data=input_dict)
for result in results:
    print('r:', result)

    for item in result:
        print('k: %s: %s' % (item, list(item.keys())))

        for key, values in item.items():
            print('kv: %s=%s' % (key, values))
