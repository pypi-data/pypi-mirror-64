# -*- coding: utf8 -*-

import os

import paddlehub as hub

from paddles.wrap import PaddleWrap

print(":: PWD: %s" % os.getcwd())

# 直接用PaddleHub提供的数据集
dataset = hub.dataset.Flowers()
paddle_wrap = PaddleWrap('xception71_imagenet', dataset)

# finetune_and_eval接口来进行模型训练，这个接口在finetune的过程中，会周期性的进行模型效果的评估，以便我们了解整个训练过程的性能变化。
run_states = paddle_wrap.task.finetune_and_eval()
results = [run_state.run_results for run_state in run_states]
for batch_result in results:
    print(batch_result)
