# coding:utf-8

import getpass
import os
from os import path

import paddlehub as hub

cpu_num = os.system('cat /proc/cpuinfo | grep "processor"| wc -l')
os.system('export CPU_NUM=%d' % (cpu_num if cpu_num else 2))

_IN_AI_STUDIO = 'aistudio' == getpass.getuser()
print(':: IN_AI_STUDIO: %s' % _IN_AI_STUDIO)

if _IN_AI_STUDIO:
    os.makedirs(path.join(os.environ['HOME'], '.paddlehub', 'cache'), exist_ok=True)


class PaddleWrap(object):

    def __init__(self, model_name, dataset: hub.dataset.BaseDataset):
        self.in_aistudio = _IN_AI_STUDIO
        self.model_name = model_name
        self.dataset = dataset

        # Load Paddlehub  pretrained model
        self.module = hub.Module(name=model_name)
        self.input_dict, self.output_dict, self.program = self.module.context(trainable=True)

        # Use ImageClassificationReader to read dataset
        data_reader = hub.reader.ImageClassificationReader(
            image_width=self.module.get_expected_image_width(),
            image_height=self.module.get_expected_image_height(),
            images_mean=self.module.get_pretrained_images_mean(),
            images_std=self.module.get_pretrained_images_std(),
            dataset=self.dataset)

        # output_dict["feature_map"]返回了resnet/mobilenet等模型对应的feature_map，可以用于图片的特征表达。
        self.feature_map = self.output_dict["feature_map"]

        # feed_list中的inputs参数指明了resnet/mobilenet等模型的输入tensor的顺序，与ImageClassifierTask返回的结果一致。
        self.feed_list = [self.input_dict["image"].name]

        # learning_rate:        全局学习率。默认为1e-4；
        # optimizer_name:       优化器名称。默认adam；
        # regularization_coeff: 正则化的λ参数。默认为1e-3；
        self.strategy = hub.DefaultFinetuneStrategy(
            learning_rate=1e-4,
            optimizer_name="adam",
            regularization_coeff=1e-3,
        )

        # log_interval:         打印训练日志的周期，默认为10。
        # eval_interval:        进行评估的周期，默认为100。
        # use_pyreader:         是否使用pyreader，默认False。
        # use_data_parallel:    是否使用并行计算，默认False。打开该功能依赖nccl库。
        # save_ckpt_interval:   保存checkpoint的周期，默认为None。
        # use_cuda:             是否使用GPU训练和评估，默认为False。
        # checkpoint_dir:       checkpoint的保存目录，默认为None，此时会在工作目录下根据时间戳生成一个临时目录。
        # num_epoch:            运行的epoch次数，默认为10。
        # batch_size：          每次训练的时候，给模型输入的每批数据大小为32，模型训练时能够并行处理批数据，
        #                       因此batch_size越大，训练的效率越高，但是同时带来了内存的负荷，过大的batch_size可能导致内存不足而无法训练，
        #                       因此选择一个合适的batch_size是很重要的一步；
        # enable_memory_optim:  是否进行内存优化，默认为False。
        # strategy:             finetune的策略。默认为None，此时会使用DefaultFinetuneStrategy策略。
        self.config = hub.RunConfig(
            use_cuda=self.in_aistudio,
            num_epoch=10,
            batch_size=32,
            log_interval=10,
            eval_interval=50,
            checkpoint_dir='../app/ckpt_model',
            strategy=self.strategy)

        # hub.ImageClassifierTask通过输入特征，label与迁移的类别数，可以生成适用于图像分类的迁移任务ImageClassifierTask。
        self.task = hub.ImageClassifierTask(
            data_reader=data_reader,
            feed_list=self.feed_list,
            feature=self.feature_map,
            num_classes=dataset.num_labels,
            config=self.config)
