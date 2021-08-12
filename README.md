# 数据转化

重要介绍

仅仅对于labelme标注工具产生的文件

本仓库包含以下内容：

1. 在label_adjust.py中能够对错误标签进行转化。
2. 在label_adjust.py中能够对类别数量进行统计。
3. 在rotated_adjust能够将十字标注转化为旋转的进行框，针对已存在标签和未存在标签都适用。

## 内容列表

- [安装](#安装)
- [使用说明](#使用说明)
	- [生成器](#生成器)

## 安装

创建虚拟环境

```sh
$ conda create -n convert python=3.8 -y
```

安装依赖

```sh
$ pip install -r requirement.txt
```
## 使用说明

输出每个类的数量

```sh
$ python labels_adjust.py --dir your dataset file
```




