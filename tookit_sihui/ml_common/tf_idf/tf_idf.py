# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/19 21:32
# @author   :Mo
# @function :tf-idf


from tookit_sihui.utils.file_utils import save_json
from tookit_sihui.utils.file_utils import load_json
from tookit_sihui.utils.file_utils import txt_write
from tookit_sihui.utils.file_utils import txt_read
import jieba
import json
import math
import os


from tookit_sihui.conf.logger_config import get_logger_root
logger = get_logger_root()


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
                    tf_char[str(char).encode('utf-8', 'ignore').decode('utf-8')] = 1
                else:
                    tf_char[str(char).encode('utf-8', 'ignore').decode('utf-8')] = tf_char[char] + 1
    tf_char['[LENS]'] = sum([v for k,v in tf_char.items()])
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
    idf_char['[LENS]'] = len(questions) # 保存一个所有的句子长度
    return idf_char


def count_tf_idf(freq_char, freq_document, ndigits=12, smooth =0):
    """
        统计tf-idf
    :param freq_char: dict, tf
    :param freq_document: dict, idf
    :return: dict, tf-idf
    """

    len_tf = freq_char['[LENS]']
    len_tf_mid = int(len(freq_char)/2)
    len_idf = freq_document['[LENS]']
    len_idf_mid = int(len(freq_document) / 2)
    # tf
    tf_char = {}
    for k2, v2 in freq_char.items():
        tf_char[k2] = round((v2 + smooth)/(len_tf + smooth), ndigits)
    # idf
    idf_char = {}
    for ki, vi in freq_document.items():
        idf_char[ki] = round(math.log((len_idf + smooth) / (vi + smooth), 2), ndigits)
    # tf-idf
    tf_idf_char = {}
    for kti, vti in freq_char.items():
        tf_idf_char[kti] = round(tf_char[kti] * idf_char[kti], ndigits)

    # 删去文档数统计
    tf_char.pop('[LENS]')
    idf_char.pop('[LENS]')
    tf_idf_char.pop('[LENS]')

    # 计算平均/最大/中位数
    tf_char_values = tf_char.values()
    idf_char_values = idf_char.values()
    tf_idf_char_values = tf_idf_char.values()

    tf_char['[AVG]'] = round(sum(tf_char_values) / len_tf, ndigits)
    idf_char['[AVG]'] = round(sum(idf_char_values) / len_idf, ndigits)
    tf_idf_char['[AVG]'] = round(sum(tf_idf_char_values) / len_idf, ndigits)
    tf_char['[MAX]'] = max(tf_char_values)
    idf_char['[MAX]'] = max(idf_char_values)
    tf_idf_char['[MAX]'] = max(tf_idf_char_values)
    tf_char['[MIN]'] = min(tf_char_values)
    idf_char['[MIN]'] = min(idf_char_values)
    tf_idf_char['[MIN]'] = min(tf_idf_char_values)
    tf_char['[MID]'] = sorted(tf_char_values)[len_tf_mid]
    idf_char['[MID]'] = sorted(idf_char_values)[len_idf_mid]
    tf_idf_char['[MID]'] = sorted(tf_idf_char_values)[len_idf_mid]

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


def save_tf_idf_json(path_dir, tf_freq, idf_freq, tf_char, idf_char, tf_idf_char):
    """
        json排序和保存
    :param path_dir:str, 保存文件目录 
    :param tf_char: dict, tf
    :param idf_char: dict, idf
    :param tf_idf_char: dict, tf-idf
    :return: None
    """
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    # freq
    save_json([tf_freq], path_dir + '/tf_freq.json')
    save_json([idf_freq], path_dir + '/idf_freq.json')
    # json_tf = json.dumps([tf_char])
    save_json([tf_char], path_dir + '/tf.json')
    # json_idf = json.dumps([idf_char])
    save_json([idf_char], path_dir + '/idf.json')
    # json_tf_idf = json.dumps([tf_idf_char])
    save_json([tf_idf_char], path_dir + '/tf_idf.json')


def load_tf_idf_json(path_tf_freq=None, path_idf_freq=None, path_tf=None, path_idf=None, path_tf_idf=None):
    """
        从json文件下载tf, idf, tf_idf
    :param path_tf: 
    :param path_idf: 
    :param path_tf_idf: 
    :return: 
    """
    json_tf_freq = load_json(path_tf_freq)
    json_idf_freq = load_json(path_idf_freq)
    json_tf = load_json(path_tf)
    json_idf = load_json(path_idf)
    json_tf_idf = load_json(path_tf_idf)
    return json_tf_freq[0], json_idf_freq[0], json_tf[0], json_idf[0], json_tf_idf[0]


def dict_add(dict1, dict2):
    """
      两个字典合并
    :param dict1: 
    :param dict2: 
    :return: 
    """
    for i,j in dict2.items():
        if i in dict1.keys():
            dict1[i] += j
        else:
            dict1.update({f'{i}' : dict2[i]})
    return dict1


class TFIDF:
    def __init__(self, questions=None, path_tf=None,
                 path_idf=None, path_tf_idf=None,
                 path_tf_freq=None, path_idf_freq=None,
                 ndigits=12, smooth=0):
        """
            统计字频,或者词频tf
        :param questions: list, 输入语料, 字级别的例子:[['我', '爱', '你'], ['爱', '护', '士']]
        """
        self.esplion = 1e-16
        self.questions = questions
        self.path_tf_freq = path_tf_freq
        self.path_idf_freq = path_idf_freq
        self.path_tf=path_tf
        self.path_idf=path_idf
        self.path_tf_idf=path_tf_idf
        self.ndigits=ndigits
        self.smooth=smooth
        self.create_tfidf()

    def create_tfidf(self):
        if self.questions != None: # 输入questions list, 即corpus语料
            self.tf_freq = count_tf(self.questions)
            self.idf_freq = count_idf(self.questions)
            self.tf, self.idf, self.tfidf = count_tf_idf(self.tf_freq,
                                                         self.idf_freq,
                                                         ndigits=self.ndigits,
                                                         smooth =self.smooth)
        else: # 输入训练好的
            self.tf_freq, self.idf_freq, \
            self.tf, self.idf, self.tfidf = load_tf_idf_json(path_tf_freq = self.path_tf_freq,
                                                             path_idf_freq = self.path_idf_freq,
                                                             path_tf=self.path_tf,
                                                             path_idf=self.path_idf,
                                                             path_tf_idf=self.path_tf_idf)
        self.chars = [idf for idf in self.idf.keys()]

    def extract_tfidf_of_sentence(self, ques):
        """
            获取tf-idf
        :param ques: str
        :return: float
        """
        assert type(ques)==str
        if not ques.strip():
            return None
        ques_list = list(jieba.cut(ques.replace(' ', '').strip()))
        logger.info(ques_list)
        score = 0.0
        score_list = {}
        for char in ques_list:
            if char in self.chars:
                score = score + self.tfidf[char]
                score_list[char] = self.tfidf[char]
            else: #
                score = score + self.esplion
                score_list[char] = self.esplion
        score = score/len(ques_list)# 求平均避免句子长度不一的影响
        logger.info(score_list)
        logger.info({ques:score})
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
        ques_list = list(jieba.cut(ques.replace(' ', '').strip()))
        logger.info(ques_list)
        score = 0.0
        score_list = {}
        for char in ques_list:
            if char in self.chars:
                score = score + self.tf[char]
                score_list[char] = self.tf[char]
            else: #
                score = score + self.esplion
                score_list[char] = self.esplion
        score = score/len(ques_list)# 求平均避免句子长度不一的影响
        logger.info(score_list)
        logger.info({ques:score})
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
        ques_list = list(jieba.cut(ques.replace(' ', '').strip()))
        logger.info(ques_list)
        score = 0.0
        score_list = {}
        for char in ques_list:
            if char in self.chars:
                score = score + self.idf[char]
                score_list[char] = self.idf[char]
            else: #
                score = score + self.esplion
                score_list[char] = self.esplion
        score = score/len(ques_list) # 求平均避免句子长度不一的影响
        logger.info(score_list)
        logger.info({ques:score})
        return score


def create_TFIDF(path):
    # 测试1,根据corpus生成
    import time
    time_start = time.time()
    # 首先输入全部文本构建tf-idf,然后再拿去用
    from tookit_sihui.conf.path_config import path_tf_idf_corpus
    from tookit_sihui.utils.file_utils import txt_write, txt_read

    path_wiki = path if path else path_tf_idf_corpus
    #  测试1, tf-idf, 调用
    path_dir = 'tf_idf_freq/'
    # ques = ['大漠帝国最强', '花落惊飞羽最漂亮', '紫色Angle最有气质', '孩子气最活泼', '口袋巧克力和过路蜻蜓最好最可爱啦', '历历在目最烦恼']
    # questions = [list(q.strip()) for q in ques]
    # questions = [list(jieba.cut(que)) for que in ques]
    questions = txt_read(path_wiki)
    len_questions = len(questions)
    batch_size = 1000000
    size_trade = len_questions // batch_size
    print(size_trade)
    size_end = size_trade * batch_size
    # 计算tf-freq, idf-freq
    ques_tf_all, ques_idf_all = {}, {}
    for i, (start, end) in enumerate(zip(range(0, size_end, batch_size),
                        range(batch_size, size_end, batch_size))):
        print("第{}次".format(i))
        question = questions[start: end]
        questionss = [ques.strip().split(' ') for ques in question]
        ques_idf = count_idf(questionss)
        ques_tf = count_tf(questionss)
        print('tf_idf_{}: '.format(i) + str(time.time() - time_start))
        # 字典合并 values相加
        ques_tf_all = dict_add(ques_tf_all, ques_tf)
        ques_idf_all = dict_add(ques_idf_all, ques_idf)
        print('dict_add_{}: '.format(i) + str(time.time() - time_start))
        print('的tf:{}'.format(ques_tf_all['的']))
        print('的idf:{}'.format(ques_idf_all['的']))
    # 不足batch-size部分
    if len_questions - size_end >0:
        print("第{}次".format('last'))
        question = questions[size_end: len_questions]
        questionss = [ques.strip().split(' ') for ques in question]
        ques_tf = count_idf(questionss)
        ques_idf = count_tf(questionss)
        # tf_char, idf_char, tf_idf_char = count_tf_idf(ques_tf, ques_idf)
        ques_tf_all = dict_add(ques_tf_all, ques_tf)
        ques_idf_all = dict_add(ques_idf_all, ques_idf)
        print('{}: '.format('last') + str(time.time() - time_start))
        print('的tf:{}'.format(ques_tf_all['的']))
        print('的idf:{}'.format(ques_idf_all['的']))
    # 计算tf-idf
    tf_char, idf_char, tf_idf_char = count_tf_idf(ques_tf_all, ques_idf_all)
    print(len(tf_char))
    print('tf-idf ' + str(time.time()-time_start))
    print('tf-idf ok!')
    # 保存, tf,idf,tf-idf
    save_tf_idf_json(path_dir, ques_tf_all, ques_idf_all, tf_char, idf_char, tf_idf_char)
    gg=0


if __name__=="__main__":
    # 测试1
    path = None # 语料地址, 格式为切分后的句子, 例如'孩子 气 和 紫色 angle'
    create_TFIDF(path)

    # # 测试2, 调用class、json, input预测
    # path_dir = 'tf_idf_freq/'
    # path_tf = path_dir + '/tf.json'
    # path_idf = path_dir + '/idf.json'
    # path_tf_idf = path_dir + '/tf_idf.json'
    #
    # tfidf = TFIDF(path_tf=path_tf, path_idf=path_idf, path_tf_idf=path_tf_idf)
    # score1 = tfidf.extract_tf_of_sentence('大漠帝国')
    # score2 = tfidf.extract_idf_of_sentence('大漠帝国')
    # score3 = tfidf.extract_tfidf_of_sentence('大漠帝国')
    # print('tf: ' + str(score1))
    # print('idf: ' + str(score2))
    # print('tfidf: ' + str(score3))
    # while True:
    #     print("请输入: ")
    #     ques = input()
    #     tfidf_score = tfidf.extract_tfidf_of_sentence(ques)
    #     print('tfidf:' + str(tfidf_score))

