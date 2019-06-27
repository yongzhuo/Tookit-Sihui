# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/19 21:32
# @author   :Mo
# @function :tf-idf


from tookit_sihui.utils.file_utils import txt_write
import math
import os


def count_tf(questions):
    """
      统计字频,或者词频tf
    :param questions: list, 输入语料, 字级别的例子:[['我', '爱', '你'], ['爱', '护', '士']]
    :return: dict, 返回字频,或者词频, 形式:{'我':1, '爱':2} 
    """
    tf_char = {}
    for question in questions:
        for char in question:
            if char.strip():
                if char not in tf_char:
                    tf_char[char] = 1
                else:
                    tf_char[char] = tf_char[char] + 1
    tf_char['lens'] = sum([v for k,v in tf_char.items()])
    return tf_char


def count_idf(questions):
    """
      统计逆文档频率idf
    :param questions: list, 输入语料, 字级别的例子:[['我', '爱', '你'], ['爱', '护', '士']]
    :return: dict, 返回逆文档频率, 形式:{'我':1, '爱':2}
    """
    idf_char = {}
    for question in questions:
        question_set = set(question) # 在句子中，重复的只计数一次
        for char in question_set:
            if char.strip(): # ''不统计
                if char not in idf_char: # 第一次计数为1
                    idf_char[char] = 1
                else:
                    idf_char[char] = idf_char[char] + 1
    idf_char['lens'] = len(questions) # 保存一个所有的句子长度
    return idf_char


def count_tf_idf(freq_char, freq_document):
    """
        统计tf-idf
    :param freq_char: dict, tf
    :param freq_document: dict, idf
    :return: dict, tf-idf
    """

    len_tf = freq_char['lens']
    # tf
    tf_char = {}
    for k2, v2 in freq_char.items():
        tf_char[k2] = v2 / len_tf
    # idf
    idf_char = {}
    for ki, vi in freq_document.items():
        idf_char[ki] = math.log(freq_document['lens'] / (vi + 1), 2)
    # tf-idf
    tf_idf_char = {}
    for kti, vti in freq_char.items():
        tf_idf_char[kti] = tf_char[kti] * idf_char[kti]

    return tf_char, idf_char, tf_idf_char


def save_tf_idf_dict(path_dir, tf_char, idf_char, tf_idf_char):
    """
        排序和保存
    :param path_dir:str, 保存文件目录 
    :param tf_char: dict, tf
    :param idf_char: dict, idf
    :param tf_idf_char: dict, tf-idf
    :return: None
    """
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    # store and save
    tf_char_sorted = sorted(tf_char.items(), key=lambda d: d[1], reverse=True)
    tf_char_sorted = [tf[0] + '\t' + str(tf[1]) + '\n' for tf in tf_char_sorted]
    txt_write(tf_char_sorted, path_dir + 'tf.txt')

    idf_char_sorted = sorted(idf_char.items(), key=lambda d: d[1], reverse=True)
    idf_char_sorted = [idf[0] + '\t' + str(idf[1]) + '\n' for idf in idf_char_sorted]
    txt_write(idf_char_sorted, path_dir + 'idf.txt')

    tf_idf_char_sorted = sorted(tf_idf_char.items(), key=lambda d: d[1], reverse=True)
    tf_idf_char_sorted = [tf_idf[0] + '\t' + str(tf_idf[1]) + '\n' for tf_idf in tf_idf_char_sorted]
    txt_write(tf_idf_char_sorted, path_dir + 'tf_idf.txt')


class TFIDF:
    def __init__(self, questions):
        """
            统计字频,或者词频tf
        :param questions: list, 输入语料, 字级别的例子:[['我', '爱', '你'], ['爱', '护', '士']]
        """
        self.questions = questions
        self.create_tfidf()

    def create_tfidf(self):
        self.tf_freq = count_tf(self.questions)
        self.idf_freq = count_idf(self.questions)
        self.tf, self.idf, self.tfidf = count_tf_idf(self.tf_freq, self.idf_freq)
        self.chars = [idf[0] for idf in self.idf]

    def extract_tfidf_of_sentence(self, ques):
        """
            获取tf-idf
        :param ques: str
        :return: float
        """
        assert type(ques)==str
        if not ques.strip():
            return None
        ques_list = list(ques.replace(' ', '').strip())
        score = 0.0
        for char in ques_list:
            if char in self.chars:
                score = score + self.tfidf[char]
        return score

    def extract_tf_of_sentence(self, ques):
        """
            获取idf
        :param ques: str
        :return: float
        """
        assert type(ques)==str
        if not ques.strip():
            return None
        ques_list = list(ques.replace(' ', '').strip())
        score = 0.0
        for char in ques_list:
            if char in self.chars:
                score = score + self.tf[char]
        return score

    def extract_idf_of_sentence(self, ques):
        """
           获取idf
        :param ques: str
        :return: float
        """
        assert type(ques)==str
        if not ques.strip():
            return None
        ques_list = list(ques.replace(' ', '').strip())
        score = 0.0
        for char in ques_list:
            if char in self.chars:
                score = score + self.idf[char]
        return score


if __name__=="__main__":
    # 测试1, tf-idf, 调用
    path_dir = 'tf_idf/'
    ques = ['大漠帝国最强', '花落惊飞羽最漂亮', '紫色Angle最有气质', '孩子气最活泼', '口袋巧克力和过路蜻蜓最好最可爱啦', '历历在目最烦恼']
    questions = [list(q.strip()) for q in ques]
    # questions = [list(jieba.cut(que)) for que in ques]
    ques_tf = count_idf(questions)
    ques_idf = count_tf(questions)
    tf_char, idf_char, tf_idf_char = count_tf_idf(ques_tf, ques_idf)
    # 保存, tf,idf,tf-idf
    save_tf_idf_dict(path_dir, tf_char, idf_char, tf_idf_char)
    print(ques_tf)
    print(ques_idf)
    print(tf_char)
    print(idf_char)
    print(tf_idf_char)

    # 测试2, 调用class, input预测
    tfidf = TFIDF(questions)
    score1 = tfidf.extract_tf_of_sentence('大漠帝国')
    score2 = tfidf.extract_idf_of_sentence('大漠帝国')
    score3 = tfidf.extract_tfidf_of_sentence('大漠帝国')
    print('tf: ' + str(score1))
    print('idf: ' + str(score2))
    print('tfidf: ' + str(score3))
    while True:
        print("请输入: ")
        ques = input()
        tfidf_score = tfidf.extract_tfidf_of_sentence(ques)
        print('tfidf:' + str(tfidf_score))

