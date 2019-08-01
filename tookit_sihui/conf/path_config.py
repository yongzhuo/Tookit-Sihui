# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/28 0:24
# @author   :Mo
# @function : base path of tookit-sihui


import pathlib
import pathlib
import sys
import os

# base dir
projectdir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)
sys.path.append(projectdir)
print(projectdir)

# tf_ifdf
path_tf_idf_corpus = projectdir.replace('\\', '/') + '/data/tf_idf/wiki_corpus_10.txt'
path_tf_idf_freq = projectdir.replace('\\', '/') + '/data/tf_idf_freq/'
