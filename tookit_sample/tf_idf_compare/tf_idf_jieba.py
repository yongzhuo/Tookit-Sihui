# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/31 21:21
# @author   :Mo
# @function :


import jieba.analyse
import jieba

sentence = '大漠 帝国 和 紫色 Angle'
seg = jieba.cut(sentence)
print(seg)
tf_idf = jieba.analyse.extract_tags(sentence, withWeight=True)
print(tf_idf)

# 结果
# [('Angle', 2.988691875725), ('大漠', 2.36158258893), ('紫色', 2.10190405216), ('帝国', 1.605909794915)]


# 说明,
# 1.1 idf  jieba中的idf来自默认文件idf.txt,
#          idf默认一段话来作为一个docunment,
#          没出现过的词语的idf默认为所有idf的平均值,即为11.多
#
# 1.2 tf   tf只统计当前句子出现的频率除以所有词语数,
#          例如'大漠 帝国 和 紫色 Angle'这句话, '大漠'的tf为1/5
#          tfidf的停用词"和"去掉了
#     tf计算代码
#         freq[w] = freq.get(w, 0.0) + 1.0
#         total = sum(freq.values())
#         for k in freq:
#             kw = k.word if allowPOS and withFlag else k
#             freq[k] *= self.idf_freq.get(kw, self.median_idf) / total









