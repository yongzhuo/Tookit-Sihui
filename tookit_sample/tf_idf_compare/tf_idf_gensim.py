# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/31 21:20
# @author   :Mo
# @function :

from gensim import corpora, models
import jieba



def tfidf_from_questions(corpora_documents):
    """
        从文件读取并计算tf-idf
    :param sources_path: 
    :return: 
    """
    dictionary = corpora.Dictionary(corpora_documents)
    corpus = [dictionary.doc2bow(text) for text in corpora_documents]
    tfidf_model = models.TfidfModel(corpus)
    return dictionary, tfidf_model


def tfidf_from_corpora(sources_path):
    """
        从文件读取并计算tf-idf
    :param sources_path: 
    :return: 
    """
    from tookit_sihui.utils.file_utils import txt_read, txt_write
    questions = txt_read(sources_path)
    corpora_documents = []
    for item_text in questions:
        item_seg = list(jieba.cut(str(item_text).strip()))
        corpora_documents.append(item_seg)

    dictionary = corpora.Dictionary(corpora_documents)
    corpus = [dictionary.doc2bow(text) for text in corpora_documents]
    tfidf_model = models.TfidfModel(corpus)
    return dictionary, tfidf_model


if __name__ == '__main__':
    # test 1 from questions
    corpora_documents = [['大漠', '帝国'],['紫色', 'Angle'],['花落', '惊', '飞羽'],
                         ['我', 'm', 'o'], ['你', 'the', 'a', 'it', 'this'], ['我', '大漠']]
    dictionary, tfidf_model = tfidf_from_questions(corpora_documents)
    idfs = tfidf_model.idfs
    sentence = '大漠 大漠 大漠'
    seg = list(jieba.cut(sentence))
    bow = dictionary.doc2bow(seg)
    tfidf_vec = tfidf_model[bow]
    print(bow)
    print(tfidf_vec)
    bow = dictionary.doc2bow(['i', 'i', '大漠', '大漠', '大漠'])
    tfidf_vec = tfidf_model[bow]
    print(bow)
    print(tfidf_vec)

    # test 2 from file of text
    from tookit_sihui.conf.path_config import path_tf_idf_corpus
    dictionary, tfidf_model = tfidf_from_corpora(path_tf_idf_corpus)
    sentence = '大漠帝国'
    seg = list(jieba.cut(sentence))
    bow = dictionary.doc2bow(seg)
    tfidf_vec = tfidf_model[bow]
    print(bow)
    print(tfidf_vec)
    bow = dictionary.doc2bow(['sihui'])
    tfidf_vec = tfidf_model[bow]
    print(bow)
    print(tfidf_vec)
    gg = 0
    # 结果
    # [(12, 1)]
    # [(12, 1.0)]
    # []
    # []
    # [(172, 1), (173, 1)]
    # [(172, 0.7071067811865475), (173, 0.7071067811865475)]
    # []
    # []



# # 说明:
# 1.左边的是字典id,右边是词的tfidf,
# 2.中文版停用词(如the)、单个字母(如i)等，不会去掉
# 3.去除没有被训练到的词,如'sihui',没有出现就不会计算
# 4.计算细节
#   4.1 idf = add + log_{log\_base} \frac{totaldocs}{docfreq}, 如下:
    # eps = 1e-12, idf只取大于eps的数字
    def df2idf(docfreq, totaldocs, log_base=2.0, add=0.0):
        import numpy as np
        # np.log()什么都不写就以e为低, 由公式log(a)(b)=log(c)(b)/log(c)(a),
        # 可得函数中为log(2)(totaldocs / docfreq)
        # debug进去可以发现, 没有进行平滑处理, 即log(2)(文本数 / 词出现在文本中的个数),
        # 这也很好理解, 因为如果输入为[],则不会给出模型,出现的文本中的至少出现一次,也没有必要加1了
        return add + np.log(float(totaldocs) / docfreq) / np.log(log_base)
        # 注意self.initialize(corpus)函数
#   4.2 tf 从下面以及debug结果可以发现, gensim的tf取值是词频,
#          也就是说出现几次就取几次,如句子'大漠 大漠 大漠', '大漠'的tf就取3
#         termid_array, tf_array = [], []
#         for termid, tf in bow:
#             termid_array.append(termid)
#             tf_array.append(tf)
#
#         tf_array = self.wlocal(np.array(tf_array))
#
#         vector = [
#             (termid, tf * self.idfs.get(termid))
#             for termid, tf in zip(termid_array, tf_array)
#             if abs(self.idfs.get(termid, 0.0)) > self.eps
#         ]


