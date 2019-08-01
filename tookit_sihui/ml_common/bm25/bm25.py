# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/29 10:22
# @author   :Mo
# @function :


import jieba


class BM25:
    def __init__(self, questions=None, path_tf=None, path_idf=None, path_tf_idf=None):
        """
            统计字频,或者词频tf
        :param questions: list, 输入语料, 字级别的例子:[['我', '爱', '你'], ['爱', '护', '士']]
        """
        self.questions = questions
        self.path_tf=path_tf
        self.path_idf=path_idf
        self.path_tf_idf=path_tf_idf
        self.param_k = 1.5
        self.param_b = 0.75
        self.epsilon = 0.25
        self.avgdl = 100
        self.create_tfidf()

    def create_tfidf(self):
        """
         获取tfidf
        :return: 
        """
        from tookit_sihui.ml_common.tf_idf.tf_idf import count_tf, count_idf,count_tf_idf,load_tf_idf_json
        if self.questions: # 输入list
            self.tf_freq = count_tf(self.questions)
            self.idf_freq = count_idf(self.questions)
            self.tf, self.idf, self.tfidf = count_tf_idf(self.tf_freq, self.idf_freq)
        else: # 输入训练好的
            _, _, self.tf, self.idf, self.tfidf = load_tf_idf_json(path_tf=self.path_tf, path_idf=self.path_idf, path_tf_idf=self.path_tf_idf)
        self.chars = [idf for idf in self.idf.keys()]
        self.lens = len(self.chars)

    def bm25_sim(self, sentence):
        """
            bm25分数
        :param sentence: 
        :return: 
        """
        sentences = list(jieba.cut(sentence))
        score = 0
        for word in sentences:
            if word in self.chars:
                tf = self.tf[word]
                idf = self.idf[word]
            else:
                tf = self.epsilon * 1e-12
                idf = self.epsilon
            score += (idf*tf*(self.param_k+1)
                      / (tf+self.param_k*(1-self.param_b+self.param_b*self.lens
                     / self.avgdl)))
        return score

    def bm25_sim_list(self, sentences):
        """
            bm25分数 list
        :param sentences: 
        :return: 
        """
        scores = []
        for sentence in sentences:
            score = self.bm25_sim(sentence)
            scores.append(score)
        return scores


if __name__ == '__main__':
    from tookit_sihui.conf.path_config import path_tf_idf_freq
    path_dir = path_tf_idf_freq # 'tf_idf_freq/'
    path_tf = path_dir + '/tf.json'
    path_idf = path_dir + '/idf.json'
    path_tf_idf = path_dir + '/tf_idf.json'
    bm25 = BM25(path_tf=path_tf, path_idf=path_idf, path_tf_idf=path_tf_idf)
    print(bm25.bm25_sim('打磨丢哦'))

    while True:
        print('请输入:')
        ques = input()
        score = bm25.bm25_sim(ques)
        print(score)